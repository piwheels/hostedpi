from typing import Union
import urllib.parse
from time import sleep

from requests import Session, HTTPError
from pydantic import ValidationError
from structlog import get_logger

from .auth import MythicAuth
from .pi import Pi
from .utils import parse_ssh_keys
from .exc import HostedPiException
from .models.responses import (
    ServersResponse,
    ErrorResponse,
    PiImagesResponse,
    ProvisioningServer,
    PiInfoResponse,
)
from .models.payloads import NewPi3ServerBody, NewPi4ServerBody, NewServer
from .logger import log_request


logger = get_logger()


OUT_OF_STOCK = "No servers with the required specification are available"


class PiCloud:
    """
    A connection to the Mythic Beasts Pi Cloud API for creating and managing cloud Pi services.

    Set up API keys at https://www.mythic-beasts.com/customer/api-users

    :type api_id: str or None
    :param api_id:
        Your Mythic Beasts API ID (alternatively, the environment variable ``HOSTEDPI_ID`` can be
        used)

    :type api_secret: str or None
    :param api_secret:
        Your Mythic Beasts API secret (alternatively, the environment variable ``HOSTEDPI_SECRET``
        can be used)

    :type ssh_keys: list or set or None
    :param ssh_keys:
        A list/set of SSH key strings (keyword-only argument)

    :type ssh_key_path: str or None
    :param ssh_key_path:
        The path to your SSH public key (keyword-only argument)

    :type ssh_import_github: list or set or None
    :param ssh_import_github:
        A list/set of GitHub usernames to import SSH keys from (keyword-only argument)

    :type ssh_import_launchpad: list or set or None
    :param ssh_import_launchpad:
        A list/set of Launchpad usernames to import SSH keys from (keyword-only argument)

    .. note::
        If any SSH keys are provided on class initialisation, they will be used when creating Pis
        but are overriden by any passed to the :meth:`~hostedpi.picloud.PiCloud.create_pi` method.

        All SSH arguments provided will be used in combination.
    """

    def __init__(
        self,
        *,
        ssh_keys: Union[list[str], set[str], None] = None,
        ssh_key_path: Union[str, None] = None,
        ssh_import_github: Union[list[str], set[str], None] = None,
        ssh_import_launchpad: Union[list[str], set[str], None] = None,
    ):
        self._api_url = "https://api.mythic-beasts.com/beta/pi/"

        self.ssh_keys = parse_ssh_keys(
            ssh_keys, ssh_key_path, ssh_import_github, ssh_import_launchpad
        )

        self._auth = MythicAuth()

    def __repr__(self):
        return f"<PiCloud id={self._auth._settings.id}>"

    @property
    def session(self) -> Session:
        return self._auth.session

    @property
    def servers(self) -> dict[str, Pi]:
        """
        A dictionary of all Pis associated with the account, with the server name as the key and
        the :class:`~hostedpi.pi.Pi` instance as the value.
        """
        servers = self._get_servers()
        return {
            name: Pi(name, info=info, api_url=self._api_url, session=self.session)
            for name, info in servers.servers.items()
        }

    @property
    def ipv4_ssh_config(self) -> str:
        """
        A string containing the IPv4 SSH config for all Pis within the account.
        The contents could be added to an SSH config file for easy access to the
        Pis in the account.
        """
        return "\n".join(pi.data.ipv4_ssh_config for pi in self.servers.values())

    @property
    def ipv6_ssh_config(self) -> str:
        """
        A string containing the IPv6 SSH config for all Pis within the account.
        The contents could be added to an SSH config file for easy access to the
        Pis in the account.
        """
        return "\n".join(pi.ipv6_ssh_config for pi in self.servers.values())

    def create_pi(
        self,
        *,
        name: Union[str, None] = None,
        spec: Union[NewPi3ServerBody, NewPi4ServerBody],
        ssh_keys: Union[list[str], set[str], None] = None,
        ssh_key_path: Union[str, None] = None,
        ssh_import_github: Union[list[str], set[str], None] = None,
        ssh_import_launchpad: Union[list[str], set[str], None] = None,
        wait_async: bool = False,
    ) -> Pi | None:
        """
        Provision a new cloud Pi with the specified name, model, disk size and SSH keys. Return a
        new :class:`~hostedpi.pi.Pi` instance.

        :type name: str or None
        :param name:
            A unique identifier for the server. This will form part of the hostname for the server,
            and must consist only of alphanumeric characters and hyphens. If not provided, a server
            name will be automatically generated.

        :type spec: NewPi3ServerBody or NewPi4ServerBody
        :param spec:
            The spec of the Raspberry Pi to provision

        :type ssh_keys: list or set or None
        :param ssh_keys:
            A list/set of SSH key strings (keyword-only argument)

        :type ssh_key_path: str or None
        :param ssh_key_path:
            The path to your SSH public key (keyword-only argument)

        :type ssh_import_github: list or set or None
        :param ssh_import_github:
            A list/set of GitHub usernames to import SSH keys from (keyword-only argument)

        :type ssh_import_launchpad: list or set or None
        :param ssh_import_launchpad:
            A list/set of Launchpad usernames to import SSH keys from (keyword-only argument)

        .. note::
            If any SSH keys are provided on class initialisation, they will be used here but are
            overriden by any passed to this method.

        .. note::
            When requesting a Pi 3, you will either get a model 3B or 3B+. It is not possible to
            request a particular model beyond 3 or 4.
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-post-piserversidentifier
        ssh_keys_set = parse_ssh_keys(
            ssh_keys, ssh_key_path, ssh_import_github, ssh_import_launchpad
        )
        spec.ssh_key = "\r\n".join(ssh_keys_set)

        if name is None:
            url = urllib.parse.urljoin(self._api_url, "servers")
        else:
            url = urllib.parse.urljoin(self._api_url, f"servers/{name}")

        try:
            data = NewServer(name=name, spec=spec.model_dump())
        except ValidationError as exc:
            logger.error(f"Invalid server name or spec: {exc}")
            raise HostedPiException(f"Invalid server name or spec") from exc

        logger.info("Creating new server", name=name, spec=spec)
        response = self.session.post(url, json=data.spec.model_dump(exclude_none=True))
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 400:
                error = ErrorResponse.model_validate(response.json()).error
                raise HostedPiException(error) from exc
            if response.status_code == 403:
                raise HostedPiException("Not authorised to provision server") from exc
            if response.status_code == 409:
                raise HostedPiException("Server name already exists") from exc
            if response.status_code == 503:
                raise HostedPiException(OUT_OF_STOCK) from exc
            raise HostedPiException(str(exc)) from exc

        if response.status_code == 202 and "Location" in response.headers:
            return self._wait_for_new_pi(response.headers["Location"])
        else:
            logger.info("Server creation request accepted", status_url=response.headers["Location"])

    def get_operating_systems(self, *, model: int) -> dict[str, str]:
        """
        Return a dict of operating systems supported by the given Pi *model* (3 or 4). Dict keys are
        identifiers (e.g. "rpi-bookworm-armhf") which can be used when provisioning a new Pi with
        :meth:`~hostedpi.picloud.PiCloud.create_pi`; dict values are text labels of the OS/distro
        names (e.g. "Raspberry Pi OS Bookworm (32 bit)").

        :type model: int
        :param model:
            The Raspberry Pi model (3 or 4) to get operating systems for (keyword-only argument)
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piimagesmodel
        if model not in {3, 4}:
            raise HostedPiException("model must be 3 or 4")
        url = urllib.parse.urljoin(self._api_url, f"images/{model}")
        response = self.session.get(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 400:
                error = ErrorResponse.model_validate(response.json()).error
                raise HostedPiException(error) from exc
            raise HostedPiException(str(exc)) from exc

        return PiImagesResponse.model_validate(response.json()).root

    def _get_servers(self) -> ServersResponse:
        """
        Retrieve all servers associated with the account
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piservers
        url = urllib.parse.urljoin(self._api_url, "servers")

        response = self.session.get(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 403:
                raise HostedPiException("Not authorised") from exc
            raise HostedPiException(str(exc)) from exc

        return ServersResponse.model_validate(response.json())

    def _parse_status(self, data: dict) -> ProvisioningServer | PiInfoResponse | None:
        """
        Get the status of an async server creation request
        """
        try:
            return PiInfoResponse.model_validate(data)
        except ValidationError:
            pass

        try:
            return ProvisioningServer.model_validate(data)
        except ValidationError:
            logger.warn("Unexpected response from server creation status endpoint")
            return

    def _wait_for_new_pi(self, url: str) -> Pi:
        """
        Wait for a new Pi to be provisioned
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-queuepitask
        while True:
            response = self.session.get(url)
            log_request(response)
            status = self._parse_status(response.json())
            if type(status) is PiInfoResponse:
                server_name = response.request.url.split("/")[-1]
                logger.info("Got server name", server_name=server_name)
                return Pi(server_name, info=status, api_url=self._api_url, session=self.session)
            if type(status) is ProvisioningServer:
                logger.info("Server creation in progress", status=status.provision_status)
            sleep(1)
