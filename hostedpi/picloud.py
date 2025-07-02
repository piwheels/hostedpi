from typing import Union
import urllib.parse

from requests import Session, HTTPError
from pydantic import ValidationError
from structlog import get_logger

from .auth import MythicAuth
from .pi import Pi
from .utils import get_error_message
from .exc import HostedPiException
from .models.sshkeys import SSHKeySources
from .models.responses import ServersResponse, PiImagesResponse, PiInfoBasic
from .models.payloads import NewServer, Pi3ServerSpec, Pi4ServerSpec
from .logger import log_request


logger = get_logger()


class PiCloud:
    """
    A connection to the Mythic Beasts Pi Cloud API for creating and managing cloud Pi servers.

    :type ssh_keys: :class:`~hostedpi.models.sshkeys.SSHKeys` or None
    :param ssh_keys:
        An instance of :class:`~hostedpi.models.sshkeys.SSHKeys` containing sources of SSH keys to
        use when creating new Pis. If not provided, no SSH keys will be used by default.

    .. note::
        If any SSH keys are provided on class initialisation, they will be used when creating Pis
        but are overriden by any passed to the :meth:`~hostedpi.picloud.PiCloud.create_pi` method.
    """

    def __init__(
        self,
        ssh_keys: Union[SSHKeySources, None] = None,
        *,
        api_url: str = "https://api.mythic-beasts.com/beta/pi/",
    ):
        self._api_url = api_url
        self.ssh_keys = None
        if ssh_keys is not None:
            if not isinstance(ssh_keys, SSHKeySources):
                raise TypeError("ssh_keys must be an instance of SSHKeySources or None")
            self.ssh_keys = ssh_keys.collect()
        self._auth = MythicAuth()

    def __repr__(self):
        return f"<PiCloud id={self._auth._settings.id}>"

    @property
    def session(self) -> Session:
        return self._auth.session

    @property
    def pis(self) -> dict[str, Pi]:
        """
        A dict of all Raspberry Pi servers associated with the account, keyed by their names.
        Each value is an instance of :class:`~hostedpi.pi.Pi` representing the server.
        """
        servers = self._get_pis()
        return {
            name: Pi(name, info=info, api_url=self._api_url, session=self.session)
            for name, info in servers.items()
        }

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
        spec: Union[Pi3ServerSpec, Pi4ServerSpec],
        ssh_keys: Union[SSHKeySources, None] = None,
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

        :type spec: Pi3ServerSpec or Pi4ServerSpec
        :param spec:
            The spec of the Raspberry Pi to provision

        :type ssh_keys: :class:`~hostedpi.models.sshkeys.SSHKeySources` or None
        :param ssh_keys:
            An instance of :class:`~hostedpi.models.sshkeys.SSHKeySources` containing sources of SSH
            keys to use when creating a new Pi. If not provided, no SSH keys will be added on
            creation.

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
        if name is None:
            # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-post-piservers
            url = urllib.parse.urljoin(self._api_url, "servers")
        else:
            # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-post-piserversidentifier
            url = urllib.parse.urljoin(self._api_url, f"servers/{name}")

        if not isinstance(spec, (Pi3ServerSpec, Pi4ServerSpec)):
            raise TypeError("spec must be an instance of Pi3ServerSpec or Pi4ServerSpec")

        if ssh_keys is not None:
            if not isinstance(ssh_keys, SSHKeySources):
                raise TypeError("ssh_keys must be an instance of SSHKeySources or None")
            ssh_keys = ssh_keys.collect()
        else:
            ssh_keys = self.ssh_keys

        try:
            data = NewServer(name=name, spec=spec, ssh_keys=ssh_keys)
        except ValidationError as exc:
            logger.error(f"Invalid server name or spec: {exc}")
            raise HostedPiException("Invalid server name or spec") from exc

        num_ssh_keys = len(ssh_keys) if ssh_keys else 0
        logger.info("Creating new server", name=name, spec=spec, ssh_keys=num_ssh_keys)
        response = self.session.post(url, json=data.payload)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            raise HostedPiException(error) from exc

        status_url = response.headers["Location"]

        logger.info("Server creation request accepted", status_url=status_url)
        basic_info = PiInfoBasic.model_validate(spec)
        pi = Pi(
            name=name,
            info=basic_info,
            api_url=self._api_url,
            session=self.session,
            status_url=status_url,
        )
        if wait:
            pi.wait_until_provisioned()
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

    def _get_pis(self) -> dict[str, PiInfoBasic]:
        """
        Retrieve all Raspberry Pi servers associated with the account
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

        response = ServersResponse.model_validate(response.json())
        return response.servers
