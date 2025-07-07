import urllib.parse
from typing import Union

from pydantic import ValidationError
from requests import HTTPError, Session
from structlog import get_logger

from .auth import MythicAuth
from .exc import (
    HostedPiInvalidParametersError,
    HostedPiNameExistsError,
    HostedPiNotAuthorizedError,
    HostedPiOutOfStockError,
    HostedPiServerError,
    HostedPiUserError,
    HostedPiValidationError,
)
from .logger import log_request
from .models.mythic.payloads import NewServer
from .models.mythic.responses import (
    PiImagesResponse,
    PiInfoBasic,
    ServerSpec,
    ServersResponse,
    SpecsResponse,
)
from .models.specs import Pi3ServerSpec, Pi4ServerSpec
from .models.sshkeys import SSHKeySources
from .pi import Pi
from .utils import get_error_message


logger = get_logger()


class PiCloud:
    """
    A connection to the Mythic Beasts Pi Cloud API for creating and managing cloud Pi servers.

    :type ssh_keys: :class:`~hostedpi.models.sshkeys.SSHKeySources` or None
    :param ssh_keys:
        An instance of :class:`~hostedpi.models.sshkeys.SSHKeySources` containing sources of SSH
        keys to use when creating new Pis. If not provided, no SSH keys will be used by default.

    :type auth: :class:`~hostedpi.auth.MythicAuth` or None
    :param auth:
        An instance of :class:`~hostedpi.auth.MythicAuth` to use for authentication with the API.
        If not provided, a default instance will be created. You almost certainly won't need to
        set this yourself.

    .. note::
        If any SSH keys are provided on class initialisation, they will be used when creating Pis
        but are overriden by any passed to the :meth:`~hostedpi.picloud.PiCloud.create_pi` method.
    """

    def __init__(
        self,
        ssh_keys: Union[SSHKeySources, None] = None,
        *,
        auth: Union[MythicAuth, None] = None,
    ):
        self.ssh_keys = None
        if ssh_keys is not None:
            if not isinstance(ssh_keys, SSHKeySources):
                raise TypeError("ssh_keys must be an instance of SSHKeySources or None")
            self.ssh_keys = ssh_keys.collect()
        if auth is None:
            auth = MythicAuth()
        self._auth = auth
        self._api_url = str(auth.settings.api_url)

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

        :raises HostedPiNotAuthorizedError:
            If the user is not authorized to retrieve the list of Pis

        :raises HostedPiServerError:
            If there is an error retrieving the list from the server
        """
        servers = self._get_pis()
        return {
            name: Pi(name, info=info, auth=self._auth) for name, info in sorted(servers.items())
        }

    @property
    def ipv4_ssh_config(self) -> str:
        """
        A string containing the IPv4 SSH config for all Pis within the account. The contents could
        be added to an SSH config file for easy access to the Pis in the account.
        """
        return "\n".join(pi.ipv4_ssh_config for pi in self.pis.values())

    @property
    def ipv6_ssh_config(self) -> str:
        """
        A string containing the IPv6 SSH config for all Pis within the account. The contents could
        be added to an SSH config file for easy access to the Pis in the account.
        """
        return "\n".join(pi.ipv6_ssh_config for pi in self.pis.values())

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
            request a particular model beyond 3 or 4. Some memory and CPU speed options are
            available when requesting a Pi 4.

        :raises HostedPiValidationError:
            If the provided name or spec is invalid

        :raises HostedPiInvalidParametersError:
            If the provided parameters are invalid, such as an unsupported model or disk size

        :raises HostedPiNotAuthorizedError:
            If the user is not authorized to create a new Pi server

        :raises HostedPiOutOfStockError:
            If there are no available Pi servers of the requested type

        :raises HostedPiServerError:
            If there is another error from the server
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
            raise HostedPiValidationError("Invalid server name or spec") from exc

        num_ssh_keys = len(ssh_keys) if ssh_keys else 0
        logger.info("Creating new server", name=name, spec=spec, ssh_keys=num_ssh_keys)
        response = self.session.post(url, json=data.payload)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            if response.status_code == 400:
                raise HostedPiInvalidParametersError(error) from exc
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            if response.status_code == 409:
                raise HostedPiNameExistsError(error) from exc
            if response.status_code == 503:
                raise HostedPiOutOfStockError(error) from exc
            raise HostedPiServerError(error) from exc

        status_url = response.headers["Location"]

        logger.info("Server creation request accepted", status_url=status_url)
        basic_info = PiInfoBasic.model_validate(spec)
        pi = Pi(
            name=name,
            info=basic_info,
            auth=self._auth,
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

        :raises HostedPiUserError:
            If the provided model is not 3 or 4

        :raises HostedPiServerError:
            If there is an error retrieving the operating systems from the server
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piimagesmodel
        if model not in {3, 4}:
            raise HostedPiUserError("model must be 3 or 4")
        url = urllib.parse.urljoin(self._api_url, f"images/{model}")
        response = self.session.get(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            raise HostedPiServerError(error) from exc

        return PiImagesResponse.model_validate(response.json()).root

    def _get_available_specs(self) -> list[ServerSpec]:
        """
        Retrieve all available Raspberry Pi server specifications

        :raises HostedPiServerError:
            If there is an error retrieving the specifications from the server
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-pimodels
        url = urllib.parse.urljoin(self._api_url, "models")
        response = self.session.get(url)
        log_request(response)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            error = get_error_message(exc)
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            raise HostedPiServerError(error) from exc

        data = SpecsResponse.model_validate(response.json())
        return data.models

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
            if response.status_code == 403:
                raise HostedPiNotAuthorizedError(error) from exc
            raise HostedPiServerError(error) from exc

        response = ServersResponse.model_validate(response.json())
        return response.servers
