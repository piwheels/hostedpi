from time import sleep
from typing import Union
import urllib.parse
from functools import cached_property
from ipaddress import IPv6Address, IPv6Network
from datetime import timezone, datetime

from requests import Session, HTTPError, ConnectionError
from structlog import get_logger
from pydantic import ValidationError

from .utils import parse_ssh_keys, get_error_message
from .exc import HostedPiException
from .models.responses import PiInfoBasic, PiInfo, SSHKeysResponse, ProvisioningServer
from .models.payloads import SSHKeyBody
from .logger import log_request


logger = get_logger()


class Pi:
    """
    The ``Pi`` class represents a single Raspberry Pi service in the Mythic Beasts Pi cloud.
    Initialising a ``Pi`` object does not provision a new Pi, rather initialisation is for internal
    construction only.

    There are two ways to get access to a ``Pi`` object: retrieval from the
    :attr:`~hostedpi.picloud.PiCloud.pis` dictionary; and the return value of
    :meth:`~hostedpi.picloud.PiCloud.create_pi` method``.

    With a ``Pi`` object, you can access data about that particular Pi service, add SSH keys, reboot
    it, cancel it and more.

    .. note::
        The ``Pi`` class should not be initialised by the user, only internally within the module.
    """

    def __init__(
        self, name: Union[str, None], *, info: PiInfoBasic, api_url: str, session: Session
    ):
        self._name = name
        self._model = info.model
        self._memory = info.memory
        self._cpu_speed = info.cpu_speed
        self._api_url = api_url
        self._session = session
        self._cancelled = False
        self._info: Union[PiInfo, None] = None
        self._last_fetched_info: Union[datetime, None] = None
        self._status_url: Union[str, None] = None

    @classmethod
    def from_pi_info(cls, name: str, *, info: PiInfo, api_url: str, session: Session):
        """
        Construct a ``Pi`` object from a :class:`~hostedpi.models.responses.PiInfo` object
        """
        basic_info = PiInfoBasic.model_validate(info)
        pi = cls(name, info=basic_info, api_url=api_url, session=session)
        pi._info = info
        pi._last_fetched_info = datetime.now(timezone.utc)
        return pi

    @classmethod
    def from_status_url(cls, *, info: PiInfo, api_url: str, session: Session, status_url: str):
        """
        Construct a ``Pi`` object from a :class:`~hostedpi.models.responses.PiInfo` object
        """
        basic_info = PiInfoBasic.model_validate(info)
        pi = cls(name=None, info=basic_info, api_url=api_url, session=session)
        pi._status_url = status_url
        return pi

    def __repr__(self):
        if self._cancelled:
            return f"<Pi name={self.name} cancelled>"
        else:
            if self._info is None:
                return f"<Pi name={self.name}>"
            model = self.model_full if self.model_full else self.model
            return f"<Pi name={self.name} model={model}>"

    @property
    def session(self) -> Session:
        """
        The authenticated requests session used to communicate with the API
        """
        return self._session

    @property
    def info(self) -> PiInfo:
        """
        The full Pi information as a :class:`~hostedpi.models.responses.PiInfo` object. Always fetch
        the latest information from the API when this is called.
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
    def memory(self) -> Union[int, None]:
        """
        The Pi's RAM size in MB
        """
        return self._memory

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
        if self.provision_status != "live":
            return f"Provisioning: {self.provision_status}"
        if self.info.boot_progress:
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
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piserversidentifierssh-key
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}/ssh-key")
        response = self.session.get(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 500:
                logger.debug(
                    "Failed to fetch SSH keys, maybe the Pi is initialising", name=self.name
                )
            else:
                error = get_error_message(exc)
                raise HostedPiException(error) from exc

        data = SSHKeysResponse.model_validate(response.json())

        return data.keys

    @ssh_keys.setter
    def ssh_keys(self, ssh_keys: Union[set[str], None]):
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-put-piserversidentifierssh-key
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}/ssh-key")
        ssh_keys_str = "\n".join(ssh_keys) if ssh_keys else None
        data = SSHKeyBody(ssh_key=ssh_keys_str)

        response = self.session.put(url, json=data.model_dump())
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            raise HostedPiException(error) from exc

    def on(self, *, wait: bool = False) -> Union[bool, None]:
        """
        Power the Pi on. If *wait* is ``False`` (the default), return immediately. If *wait* is
        ``True``, wait until the power on request is completed, and return ``True`` on success, and
        ``False`` on failure.
        """
        self._power_on_off(on=True)
        if wait:
            while self.info.is_booting:
                sleep(5)
            return self.power

    def off(self):
        """
        Power the Pi off and return immediately
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
                raise HostedPiException(error) from exc

        if wait:
            while self.info.is_booting:
                sleep(5)
            return self.power

    def cancel(self):
        """
        Cancel the Pi service
        """
        if self._cancelled:
            logger.warn("This Pi server is already cancelled", name=self.name)
            return

        # check if the server is still provisioning
        status = self.get_provision_status()
        if type(status) is not PiInfo:
            logger.warn("Cannot cancel a server that is still provisioning", name=self.name)
            return

        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-delete-piserversidentifier
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}")
        response = self.session.delete(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            raise HostedPiException(error) from exc

        self._cancelled = True

    def ssh_import_id(
        self,
        *,
        github: Union[set[str], None] = None,
        launchpad: Union[set[str], None] = None,
    ) -> set[str]:
        """
        Import SSH keys from GitHub or Launchpad, and add them to the Pi. Return the set of keys
        added.

        :type ssh_import_github: set[str] or None
        :param ssh_import_github:
            A list/set of GitHub usernames to import SSH keys from (keyword-only argument)

        :type ssh_import_launchpad: set[str] or None
        :param ssh_import_launchpad:
            A list/set of Launchpad usernames to import SSH keys from (keyword-only argument)
        """
        ssh_keys_set = parse_ssh_keys(
            ssh_import_github=github,
            ssh_import_launchpad=launchpad,
        )
        self.ssh_keys |= ssh_keys_set
        return ssh_keys_set

    def wait_until_provisioned(self):
        """
        Wait for the new Pi to be provisioned
        """
        while True:
            pi_info = self.get_provision_status()
            if type(pi_info) is PiInfo:
                return
            sleep(5)

    def get_provision_status(self) -> Union[str, PiInfo, None]:
        """
        Send a request to the server creation status endpoint and return the status as either a
        string or :class:`~hostedpi.models.responses.PiInfo` or ``None`` if the status is not yet
        available.
        """
        if self._status_url is None:
            return self.info

        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-queuepitask
        try:
            response = self.session.get(self._status_url)
            response.raise_for_status()
        except ConnectionError as exc:
            logger.warn("Error getting server provisioning status", exc=str(exc))
            return
        except HTTPError as exc:
            error = get_error_message(exc)
            raise HostedPiException(error) from exc

        log_request(response)

        status = self._parse_status(response.json())
        if type(status) is ProvisioningServer:
            logger.info("Server provisioning in progress", status=status.provision_status)
            return status.provision_status
        if type(status) is PiInfo:
            self._name = response.request.url.split("/")[-1]
            self._info = status
            self._last_fetched_info = datetime.now(timezone.utc)
            self._status_url = None
            logger.info("Got server name", server_name=self._name)
            return status

    def _get_info(self):
        """
        Fetch the full Pi information from the API
        """
        if self.name is None:
            raise HostedPiException("Cannot fetch info for a Pi without a name")
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
            raise HostedPiException(error) from exc

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
            raise HostedPiException(error) from exc

    def _parse_status(self, data: dict) -> Union[ProvisioningServer, PiInfo, None]:
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
