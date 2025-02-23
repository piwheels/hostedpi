from typing import Union, Any
import urllib.parse
from pathlib import Path

from requests import Session, HTTPError
from pydantic import ValidationError
from structlog import get_logger

from .auth import MythicAuth
from .pi import Pi
from .utils import parse_ssh_keys, get_error_message
from .exc import HostedPiException
from .models.responses import ServersResponse, PiImagesResponse, PiInfoBasic
from .models.payloads import NewPi3ServerBody, NewPi4ServerBody, NewServer
from .logger import log_request


logger = get_logger()


class PiCloud:
    """
    A connection to the Mythic Beasts Pi Cloud API for creating and managing cloud Pi servers.

    :type ssh_keys: set[str] or None
    :param ssh_keys:
        A list/set of SSH key strings (keyword-only argument)

    :type ssh_key_path: Path or str or None
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

        self.ssh_keys = parse_ssh_keys(
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
    def pis(self) -> list[Pi]:
        """
        A list of all Raspberry Pi servers associated with the account, as :class:`~hostedpi.pi.Pi`
        instances
        """
        servers = self._get_servers()
        pis = [
            Pi(name, info=info, api_url=self._api_url, session=self.session)
            for name, info in servers.servers.items()
        ]
        return sorted(pis, key=lambda pi: pi.name)

    @property
    def ipv4_ssh_config(self) -> str:
        """
        A string containing the IPv4 SSH config for all Pis within the account. The contents could
        be added to an SSH config file for easy access to the Pis in the account.
        """
        return "\n".join(pi.ipv4_ssh_config for pi in self.pis)

    @property
    def ipv6_ssh_config(self) -> str:
        """
        A string containing the IPv6 SSH config for all Pis within the account. The contents could
        be added to an SSH config file for easy access to the Pis in the account.
        """
        return "\n".join(pi.ipv6_ssh_config for pi in self.pis)

    def create_pi(
        self,
        *,
        name: Union[str, None] = None,
        spec: dict[str, Any],
        ssh_keys: Union[set[str], None] = None,
        ssh_key_path: Union[Path, str, None] = None,
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

        :type spec: dict
        :param spec:
            The spec of the Raspberry Pi to provision - must be compatible with the
            :class:`~hostedpi.models.NewPi3ServerBody` or
            :class:`~hostedpi.models.NewPi4ServerBody` models.

        :type ssh_keys: set[str] or None
        :param ssh_keys:
            A list/set of SSH key strings (keyword-only argument)

        :type ssh_key_path: Path or str or None
        :param ssh_key_path:
            The path to your SSH public key (keyword-only argument)

        :type ssh_import_github: set[str] or None
        :param ssh_import_github:
            A list/set of GitHub usernames to import SSH keys from (keyword-only argument)

        :type ssh_import_launchpad: set[str] or None
        :param ssh_import_launchpad:
            A list/set of Launchpad usernames to import SSH keys from (keyword-only argument)

        :type wait: bool
        :param wait:
            If True, the method will return immediately after the server creation request is
            accepted, without waiting for the server to be provisioned. The returned
            :class:`~hostedpi.pi.Pi` instance will not be fully initialised and will not be able to
            perform actions until the server is ready. If False, the method will wait for the server
            to be provisioned before returning the :class:`~hostedpi.pi.Pi` instance. Default is
            False.

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
            spec["ssh_key"] = parse_ssh_keys(
                ssh_keys=ssh_keys,
                ssh_key_path=Path(ssh_key_path) if ssh_key_path else None,
                ssh_import_github=ssh_import_github,
                ssh_import_launchpad=ssh_import_launchpad,
            )
        elif self.ssh_keys:
            spec.ssh_key = self.ssh_keys

        if spec["model"] == 3:
            validated_spec = NewPi3ServerBody.model_validate(spec)
        elif spec["model"] == 4:
            validated_spec = NewPi4ServerBody.model_validate(spec)
        else:
            raise TypeError("Model must be 3 or 4")

        if name is None:
            url = urllib.parse.urljoin(self._api_url, "servers")
        else:
            url = urllib.parse.urljoin(self._api_url, f"servers/{name}")

        try:
            data = NewServer(name=name, spec=validated_spec)
        except ValidationError as exc:
            logger.error(f"Invalid server name or spec: {exc}")
            raise HostedPiException(f"Invalid server name or spec") from exc

        logger.info("Creating new server", name=name, spec=validated_spec)
        response = self.session.post(url, json=data.spec.model_dump(exclude_none=True))
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            raise HostedPiException(error) from exc

        logger.info("Server creation request accepted", status_url=response.headers["Location"])
        info = PiInfoBasic.model_validate(validated_spec)
        pi = Pi(name, info=info, api_url=self._api_url, session=self.session)

        if wait:
            pi.wait_until_provisioned(response.headers["Location"])
        return pi

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
