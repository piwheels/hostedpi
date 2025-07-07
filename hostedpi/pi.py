import urllib.parse
from datetime import datetime, timezone
from functools import cached_property
from ipaddress import IPv6Address, IPv6Network
from time import sleep
from typing import Union

from pydantic import ValidationError
from requests import ConnectionError, HTTPError, Session
from structlog import get_logger

from .auth import MythicAuth
from .exc import (
    HostedPiNotAuthorizedError,
    HostedPiProvisioningError,
    HostedPiServerError,
    HostedPiUserError,
)
from .logger import log_request
from .models.mythic.responses import (
    PiInfo,
    PiInfoBasic,
    ProvisioningServer,
    SSHKeysResponse,
)
from .models.sshkeys import SSHKeySources
from .utils import (
    dedupe_ssh_keys,
    get_error_message,
    remove_imported_ssh_keys,
    remove_ssh_keys_by_label,
)


logger = get_logger()


class Pi:
    """
    The ``Pi`` class represents a single Raspberry Pi service in the Mythic Beasts Pi cloud.
    Initialising a ``Pi`` object does not provision a new Pi, rather initialisation is for internal
    construction only.

    There are two ways to get access to a ``Pi`` object: retrieval from the
    :attr:`~hostedpi.picloud.PiCloud.pis` dictionary; and the return value of
    :meth:`~hostedpi.picloud.PiCloud.create_pi` method.

    With a ``Pi`` object, you can access data about that particular Pi service, add SSH keys, reboot
    it, cancel it and more.

    .. note::
        The ``Pi`` class should not be initialised by the user, only internally within the module
    """

    def __init__(
        self,
        name: Union[str, None],
        *,
        info: PiInfoBasic,
        auth: Union[MythicAuth, None] = None,
        status_url: Union[str, None] = None,
    ):
        self._name = name
        self._model = info.model
        self._memory = info.memory
        self._cpu_speed = info.cpu_speed
        if auth is None:
            auth = MythicAuth()
        self._auth = auth
        self._api_url = str(auth.settings.api_url)
        self._cancelled = False
        self._info: Union[PiInfoBasic, PiInfo, None] = None
        self._last_fetched_info: Union[datetime, None] = None
        self._status_url: Union[str, None] = status_url

    def __repr__(self):
        if self._cancelled:
            return f"<Pi name={self.name} cancelled>"
        if self._info is None:
            return f"<Pi name={self.name} model={self.model}>"
        model = self.model_full if self.model_full else self.model
        return f"<Pi name={self.name} model={model}>"

    @property
    def session(self) -> Session:
        """
        The authenticated requests session used to communicate with the API
        """
        return self._auth.session

    @property
    def info(self) -> PiInfo:
        """
        The full Pi information as a :class:`~hostedpi.models.mythic.responses.PiInfo` object.
        Always fetches the latest information from the API when this is called (with a cache timeout
        of 10 seconds).

        :raises HostedPiUserError:
            If the Pi has not been initialised with a name yet, or if the name is ``None``

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server info

        :raises HostedPiProvisioningError:
            If there is an error retrieving the Pi information from the API because the Pi is still
            provisioning

        :raises HostedPiServerError:
            If there is another error retrieving the Pi information from the API
        """
        if self._info is None:
            self._get_info()
        return self._info

    @property
    def name(self) -> str:
        """
        The name of the Pi
        """
        return self._name

    @property
    def model(self) -> int:
        """
        The Pi's model (3 or 4)
        """
        return self._model

    @cached_property
    def model_full(self) -> Union[str, None]:
        """
        The Pi's model name (3B, 3B+ or 4B)
        """
        return self.info.model_full

    @property
    def memory_mb(self) -> Union[int, None]:
        """
        The Pi's RAM size in MB
        """
        return self._memory

    @property
    def memory_gb(self) -> Union[int, None]:
        """
        The Pi's RAM size in GB
        """
        return self._memory // 1024 if self._memory else None

    @property
    def cpu_speed(self) -> Union[int, None]:
        """
        The Pi's CPU speed in MHz
        """
        return self._cpu_speed

    @cached_property
    def disk_size(self) -> Union[int, None]:
        """
        The Pi's disk size in GB
        """
        return self.info.disk_size

    @cached_property
    def nic_speed(self) -> Union[int, None]:
        """
        The Pi's NIC speed in MHz
        """
        return self.info.nic_speed

    @property
    def status(self) -> str:
        """
        A string representing the Pi's current status (provisioning, booting, live, powered on or
        powered off).
        """
        self._get_info()
        if self.provision_status != "live":
            return f"Provisioning: {self.provision_status}"
        if self.info.is_booting:
            return f"Booting: {self.boot_progress}"
        if self.power:
            return "Powered on"
        return "Powered off"

    @property
    def boot_progress(self) -> str:
        """
        A string representing the Pi's boot progress. Can be ``booted``, ``powered off`` or a
        particular stage of the boot process if currently booting.
        """
        if self.info.boot_progress:
            return self.info.boot_progress
        return "booted" if self.power else "powered off"

    @property
    def initialised_keys(self) -> bool:
        """
        A boolean representing whether or not the Pi has been initialised with SSH keys
        """
        return self.info.initialised_keys

    @cached_property
    def ipv4_ssh_port(self) -> int:
        """
        The SSH port to use when connecting via the IPv4 proxy
        """
        return self.info.ssh_port

    @cached_property
    def ipv6_address(self) -> IPv6Address:
        """
        The Pi's IPv6 address as an :class:`~ipaddress.IPv6Address` object
        """
        return self.info.ipv6_address

    @cached_property
    def ipv6_network(self) -> IPv6Network:
        """
        The Pi's IPv6 network as an :class:`~ipaddress.IPv6Network` object
        """
        return self.info.ipv6_network

    @property
    def is_booting(self) -> bool:
        """
        A boolean representing whether or not the Pi is currently booting
        """
        return self.info.is_booting

    @cached_property
    def location(self) -> str:
        """
        The Pi's physical location (data centre)
        """
        return self.info.location

    @property
    def power(self) -> bool:
        """
        A boolean representing whether or not the Pi is currently powered on
        """
        return self.info.power

    @property
    def provision_status(self) -> str:
        """
        A string representing the provision status of the Pi. Can be "provisioning", "initialising"
        or "live".
        """
        return self.info.provision_status

    @property
    def ipv4_ssh_command(self) -> str:
        """
        The SSH command required to connect to the Pi over IPv4
        """
        return f"ssh -p {self.ipv4_ssh_port} root@ssh.{self.name}.hostedpi.com"

    @property
    def ipv6_ssh_command(self) -> str:
        """
        The SSH command required to connect to the Pi over IPv6
        """
        return f"ssh root@[{self.ipv6_address}]"

    @property
    def ipv4_ssh_config(self) -> str:
        """
        A string containing the IPv4 SSH config for the Pi. The contents could be added to an SSH
        config file for easy access to the Pi.
        """
        return f"""Host {self.name}
    user root
    port {self.ipv4_ssh_port}
    hostname ssh.{self.name}.hostedpi.com
        """.strip()

    @property
    def ipv6_ssh_config(self) -> str:
        """
        A string containing the IPv6 SSH config for the Pi. The contents could be added to an SSH
        config file for easy access to the Pi.
        """
        return f"""Host {self.name}
    user root
    hostname {self.ipv6_address}
        """.strip()

    @property
    def url(self) -> str:
        """
        The http version of the hostedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to be resolvable.
        """
        return f"http://www.{self.name}.hostedpi.com"

    @property
    def url_ssl(self) -> str:
        """
        The https version of the hostedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to be resolvable, and an
            SSL certificate must be created.

            See https://letsencrypt.org/
        """
        return f"https://www.{self.name}.hostedpi.com"

    @property
    def ssh_keys(self) -> set[str]:
        """
        Retrieve the SSH keys on the Pi, or use assignment to update them. Property value is a set
        of strings. Assigned value should also be a set of strings, or None to unset.

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiProvisioningError:
            If the Pi is still provisioning

        :raises HostedPiServerError:
            If there is another error accessing the API

        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piserversidentifierssh-key
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}/ssh-key")
        response = self.session.get(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            if response.status_code == 409:
                raise HostedPiProvisioningError(error) from exc
            raise HostedPiServerError(error) from exc

        data = SSHKeysResponse.model_validate(response.json())

        return dedupe_ssh_keys(data.keys)

    @ssh_keys.setter
    def ssh_keys(self, ssh_keys: Union[set[str], None]):
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-put-piserversidentifierssh-key
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}/ssh-key")

        if ssh_keys is None:
            data = {"ssh_key": ""}
        else:
            data = {"ssh_key": "\r\n".join(dedupe_ssh_keys(ssh_keys))}

        response = self.session.put(url, json=data)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            if response.status_code == 409:
                raise HostedPiProvisioningError(error) from exc
            raise HostedPiServerError(error) from exc

    def on(self, *, wait: bool = False) -> Union[bool, None]:
        """
        Power the Pi on. If *wait* is ``False`` (the default), return immediately. If *wait* is
        ``True``, wait until the power on request is completed, and return ``True`` on success, and
        ``False`` on failure.

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiProvisioningError:
            If the server is still provisioning

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        self._power_on_off(on=True)
        if wait:
            while self.info.is_booting:
                sleep(10)
            return self.power

    def off(self):
        """
        Power the Pi off and return immediately

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiProvisioningError:
            If the server is still provisioning

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        self._power_on_off(on=False)

    def reboot(self, *, wait: bool = False):
        """
        Reboot the Pi. If *wait* is ``False`` (the default), return ``None`` immediately. If *wait*
        is ``True``, wait until the reboot request is completed, and return ``True`` on success, and
        ``False`` on failure.

        .. note::
            Note that if *wait* is ``False``, you can poll for the boot status while rebooting by
            inspecting the properties :attr:`~hostedpi.pi.Pi.is_booting` and
            :attr:`~hostedpi.pi.Pi.boot_progress`.

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-post-piserversidentifierreboot
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}/reboot")
        response = self.session.post(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 409:
                # The server is already being rebooted
                pass
            else:
                error = get_error_message(exc)
                if response.status_code == 403:
                    raise HostedPiNotAuthorizedError(error) from exc
                raise HostedPiServerError(error) from exc

        if wait:
            while self.info.is_booting:
                sleep(5)
            return self.power

    def cancel(self):
        """
        Unprovision the Pi server immediately

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiProvisioningError:
            If the server is still provisioning

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-delete-piserversidentifier
        if self._cancelled:
            logger.warn("This Pi server is already cancelled", name=self.name)
            return

        # check if the server is still provisioning
        status = self.get_provision_status()
        if type(status) is not PiInfo:
            logger.warn("Cannot cancel a server that is still provisioning", name=self.name)
            return

        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}")
        response = self.session.delete(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            if response.status_code == 409:
                raise HostedPiProvisioningError(error) from exc
            raise HostedPiServerError(error) from exc

        self._cancelled = True

    def add_ssh_keys(self, ssh_keys: SSHKeySources) -> set[str]:
        """
        Add SSH keys to the Pi from the specified sources.

        :type ssh_keys: SSHKeySources
        :param ssh_keys: The sources to find keys to add to the Pi

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiProvisioningError:
            If the Pi is still provisioning

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        keys = ssh_keys.collect()
        if keys:
            self.ssh_keys |= keys
        return self.ssh_keys

    def unimport_ssh_keys(
        self,
        *,
        github_usernames: Union[set[str], None] = None,
        launchpad_usernames: Union[set[str], None] = None,
    ) -> set[str]:
        """
        Remove SSH keys that were imported from GitHub or Launchpad, and return the remaining set of
        keys.

        :type github_usernames: set[str] or None
        :param github_usernames:
            A set of GitHub usernames to remove SSH keys for (keyword-only argument)

        :type launchpad_usernames: set[str] or None
        :param launchpad_usernames:
            A set of Launchpad usernames to remove SSH keys for (keyword-only argument)

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiProvisioningError:
            If the Pi is still provisioning

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        ssh_keys = self.ssh_keys
        if github_usernames:
            for username in github_usernames:
                ssh_keys = remove_imported_ssh_keys(ssh_keys, "gh", username)

        if launchpad_usernames:
            for username in launchpad_usernames:
                ssh_keys = remove_imported_ssh_keys(ssh_keys, "lp", username)

        self.ssh_keys = ssh_keys
        return self.ssh_keys

    def remove_ssh_keys(self, label: Union[str, None] = None) -> set[str]:
        """
        Remove an SSH key from the Pi that has a specific label (e.g. ``user@hostname``) and return
        the remaining set of keys. If *label* is ``None``, all keys will be removed.

        :type label: str or None
        :param label: The label of the SSH key to remove

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiProvisioningError:
            If the Pi is still provisioning

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        if label is None:
            self.ssh_keys = None
        else:
            self.ssh_keys = remove_ssh_keys_by_label(self.ssh_keys, label)
        return self.ssh_keys

    def wait_until_provisioned(self):
        """
        Wait for the new Pi to be provisioned

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        while True:
            pi_info = self.get_provision_status()
            if type(pi_info) is PiInfo:
                return
            sleep(5)

    def get_provision_status(self) -> Union[PiInfo, ProvisioningServer, None]:
        """
        Send a request to the server creation status endpoint and return the status as either a
        :class:`~hostedpi.models.mythic.responses.PiInfo` or
        :class:`~hostedpi.models.mythic.responses.ProvisioningServer` or ``None`` if the status is
        not yet available.

        :raises HostedPiNotAuthorizedError:
            If the user is not authorised to access the server

        :raises HostedPiServerError:
            If there is another error accessing the API
        """
        if self._status_url is None:
            return self.info

        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-queuepitask
        try:
            response = self.session.get(self._status_url)
        except ConnectionError as exc:
            logger.warn("Temporary error getting server provisioning status", exc=str(exc))
            return

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            raise HostedPiServerError(error) from exc

        log_request(response)

        status = self._parse_status(response.json())
        if type(status) is ProvisioningServer:
            logger.info("Server provisioning in progress", status=status.provision_status)
            return status
        if type(status) is PiInfo:
            self._name = response.request.url.split("/")[-1]
            logger.info("Server provisioning complete", server_name=self._name)
            self._info = status
            self._last_fetched_info = datetime.now(timezone.utc)
            self._status_url = None
            return status

    def _get_info(self):
        """
        Fetch the full Pi information from the API, or return immediately if the last fetch was
        less than 10 seconds ago.
        """
        if self.name is None:
            raise HostedPiUserError("Cannot fetch info for a Pi without a name")
        now = datetime.now(timezone.utc)
        if self._last_fetched_info is not None:
            if (now - self._last_fetched_info).total_seconds() < 10:
                return
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piserversidentifier
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}")
        response = self.session.get(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            if response.status_code == 409:
                raise HostedPiProvisioningError(error) from exc
            raise HostedPiServerError(error) from exc

        self._info = PiInfo.model_validate(response.json())

    def _power_on_off(self, *, on: bool):
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-put-piserversidentifierpower
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}/power")
        data = {
            "power": on,
        }
        response = self.session.put(url, json=data)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            if response.status_code == 409:
                raise HostedPiProvisioningError(error) from exc
            raise HostedPiServerError(error) from exc

    def _parse_status(self, data: dict) -> Union[PiInfo, ProvisioningServer, None]:
        """
        Get the status of an async server creation request
        """
        try:
            return PiInfo.model_validate(data)
        except ValidationError:
            pass

        try:
            return ProvisioningServer.model_validate(data)
        except ValidationError:
            logger.warn("Unexpected response from server creation status endpoint")
            return
