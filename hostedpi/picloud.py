from typing import Union
import urllib.parse
from time import sleep
from pathlib import Path

from requests import Session, HTTPError, ConnectionError
from pydantic import ValidationError
from structlog import get_logger

from .auth import MythicAuth
from .pi import Pi
from .utils import parse_ssh_keys_to_str, get_error_message
from .exc import HostedPiException
from .models.responses import (
    ServersResponse,
    PiImagesResponse,
    ProvisioningServer,
    PiInfo,
    PiInfoBasic,
)
from .models.payloads import NewPi3ServerBody, NewPi4ServerBody, NewServer
from .logger import log_request


logger = get_logger()


class PiCloud:
    """
    A connection to the Mythic Beasts Pi Cloud API for creating and managing cloud Pi services.

    :type ssh_keys: set[str] or None
    :param ssh_keys:
        A list/set of SSH key strings (keyword-only argument)

    :type ssh_key_path: str or None
    :param ssh_key_path:
        The path to your SSH public key (keyword-only argument)

    :type ssh_import_github: set[str] or None
    :param ssh_import_github:
        A list/set of GitHub usernames to import SSH keys from (keyword-only argument)

    :type ssh_import_launchpad: set[str] or None
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
        ssh_keys: Union[set[str], None] = None,
        ssh_key_path: Union[Path, None] = None,
        ssh_import_github: Union[set[str], None] = None,
        ssh_import_launchpad: Union[set[str], None] = None,
    ):
        self._api_url = "https://api.mythic-beasts.com/beta/pi/"

        self.ssh_keys = parse_ssh_keys_to_str(
            ssh_keys=ssh_keys,
            ssh_key_path=ssh_key_path,
            ssh_import_github=ssh_import_github,
            ssh_import_launchpad=ssh_import_launchpad,
        )

        self._auth = MythicAuth()

    def __repr__(self):
        return f"<PiCloud id={self._auth._settings.id}>"

    @property
    def session(self) -> Session:
        return self._auth.session

    @property
    def pis(self) -> dict[str, Pi]:
        """
        A dictionary of all Pis associated with the account, with the server name as the key and
        the :class:`~hostedpi.pi.Pi` instance as the value.
        """
        servers = self._get_servers()
        return {
            name: Pi(name, info=info, api_url=self._api_url, session=self.session)
            for name, info in sorted(servers.servers.items())
        }

    @property
    def ipv4_ssh_config(self) -> str:
        """
        A string containing the IPv4 SSH config for all Pis within the account.
        The contents could be added to an SSH config file for easy access to the
        Pis in the account.
        """
        return "\n".join(pi.info.ipv4_ssh_config for pi in self.pis.values())

    @property
    def ipv6_ssh_config(self) -> str:
        """
        A string containing the IPv6 SSH config for all Pis within the account.
        The contents could be added to an SSH config file for easy access to the
        Pis in the account.
        """
        return "\n".join(pi.ipv6_ssh_config for pi in self.pis.values())

    def create_pi(
        self,
        *,
        name: Union[str, None] = None,
        spec: Union[NewPi3ServerBody, NewPi4ServerBody],
        ssh_keys: Union[set[str], None] = None,
        ssh_key_path: Union[Path, None] = None,
        ssh_import_github: Union[set[str], None] = None,
        ssh_import_launchpad: Union[set[str], None] = None,
        wait: bool = False,
    ) -> Pi:
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

        :type ssh_keys: set[str] or None
        :param ssh_keys:
            A list/set of SSH key strings (keyword-only argument)

        :type ssh_key_path: str or None
        :param ssh_key_path:
            The path to your SSH public key (keyword-only argument)

        :type ssh_import_github: set[str] or None
        :param ssh_import_github:
            A list/set of GitHub usernames to import SSH keys from (keyword-only argument)

        :type ssh_import_launchpad: set[str] or None
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
        keys = [ssh_keys, ssh_key_path, ssh_import_github, ssh_import_launchpad]
        if any(key is not None for key in keys):
            spec.ssh_key = parse_ssh_keys_to_str(
                ssh_keys=ssh_keys,
                ssh_key_path=ssh_key_path,
                ssh_import_github=ssh_import_github,
                ssh_import_launchpad=ssh_import_launchpad,
            )
        elif self.ssh_keys:
            spec.ssh_key = self.ssh_keys

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
            error = get_error_message(exc)
            raise HostedPiException(error) from exc

        if wait:
            return self._wait_for_new_pi(response.headers["Location"])
        else:
            logger.info("Server creation request accepted", status_url=response.headers["Location"])
            info = PiInfoBasic.model_validate(spec)
            return Pi(name, info=info, api_url=self._api_url, session=self.session)

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
            error = get_error_message(exc)
            raise HostedPiException(error) from exc

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
            error = get_error_message(exc)
            raise HostedPiException(error) from exc

        return ServersResponse.model_validate(response.json())

    def _parse_status(self, data: dict) -> ProvisioningServer | PiInfo | None:
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

    def _wait_for_new_pi(self, url: str) -> Pi:
        """
        Wait for a new Pi to be provisioned
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-queuepitask
        while True:
            try:
                response = self.session.get(url)
                response.raise_for_status()
            except (HTTPError, ConnectionError) as exc:
                logger.warn("Error getting server creation status", exc=str(exc))
                sleep(5)
                continue

            log_request(response)

            status = self._parse_status(response.json())
            if type(status) is PiInfo:
                server_name = response.request.url.split("/")[-1]
                logger.info("Got server name", server_name=server_name)
                return Pi.from_pi_info(
                    server_name, info=status, api_url=self._api_url, session=self.session
                )
            if type(status) is ProvisioningServer:
                logger.info("Server creation in progress", status=status.provision_status)
            sleep(5)
