from time import sleep
from typing import Union
import urllib.parse

from requests import Session, HTTPError

from .utils import parse_ssh_keys
from .exc import HostedPiException
from .models.responses import PiInfoBasic, PiInfoResponse, SSHKeysResponse
from .models.payloads import SSHKeyBody
from .piinfo import PiInfo


NOT_AUTHORISED = "Not authorised to access server or server does not exist"
NOT_PROVISIONED = "Server is not fully provisioned"


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
        self, name: str, *, info: PiInfoBasic | PiInfoResponse, api_url: str, session: Session
    ):
        self._name = name
        self._session = session
        self._api_url = urllib.parse.urljoin(api_url, "servers")
        self._cancelled = False
        self._info_basic: PiInfoBasic
        self._info: Union[PiInfoResponse, None] = None

        if type(info) is PiInfoBasic:
            self._info_basic = info
        else:
            self._info_basic = PiInfoBasic.model_validate(info)
            self._info = info

    def __repr__(self):
        if self._cancelled:
            return f"<Pi {self.name} cancelled>"
        else:
            if self._info is None:
                return f"<Pi {self.name}>"
            model = self._info.model_full if self._info.model_full else self._info.model
            return f"<Pi model {model} {self.name}>"

    def _get_data(self):
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piserversidentifier
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}")
        response = self.session.get(url)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 403:
                raise HostedPiException(NOT_AUTHORISED) from exc
            if response.status_code == 409:
                raise HostedPiException(NOT_PROVISIONED) from exc
            raise HostedPiException(str(exc)) from exc

        data = PiInfoResponse.model_validate(response.json())
        self._info = PiInfo(self._name, data)

    @property
    def session(self) -> Session:
        return self._session

    @property
    def data(self) -> PiInfoResponse:
        if self._info is None:
            self._get_data()
        return self._info

    @property
    def name(self) -> str:
        return self._name

    @property
    def ssh_keys(self) -> set[str]:
        """
        Retrieve the SSH keys on the Pi, or use assignment to update them. Property value is a set
        of strings. Assigned value should also be a set of strings.
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piserversidentifierssh-key
        url = urllib.parse.urljoin(self._api_url, f"{self.name}/ssh-key")
        response = self.session.get(url)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 403:
                raise HostedPiException(NOT_AUTHORISED) from exc
            raise HostedPiException(str(exc)) from exc

        data = SSHKeysResponse.model_validate(response.json())

        return data.keys

    @ssh_keys.setter
    def ssh_keys(self, ssh_keys: Union[set[str], list[str]]):
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-put-piserversidentifierssh-key
        url = urllib.parse.urljoin(self._api_url, f"{self.name}/ssh-key")
        ssh_keys_str = "\n".join(ssh_keys)
        data = SSHKeyBody(ssh_key=ssh_keys_str)

        response = self.session.put(url, json=data.model_dump())

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 403:
                raise HostedPiException(NOT_AUTHORISED) from exc
            raise HostedPiException(str(exc)) from exc

    def _power_on_off(self, *, on: bool):
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-put-piserversidentifierpower
        url = urllib.parse.urljoin(self._api_url, f"{self.name}/power")
        data = {
            "power": on,
        }
        response = self.session.put(url, json=data)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 400:
                msg = "The server is already being rebooted"
                raise HostedPiException(msg) from exc
            if response.status_code == 403:
                raise HostedPiException(NOT_AUTHORISED) from exc
            raise HostedPiException(str(exc)) from exc

    def on(self, *, wait: bool = False) -> Union[bool, None]:
        """
        Power the Pi on. If *wait* is ``False`` (the default), return immediately. If *wait* is
        ``True``, wait until the power on request is completed, and return ``True`` on success, and
        ``False`` on failure.
        """
        self._power_on_off(on=True)
        if wait:
            while self._info.is_booting:
                sleep(2)
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
        url = urllib.parse.urljoin(self._api_url, f"{self.name}/reboot")
        response = self.session.post(url)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 403:
                raise HostedPiException(NOT_AUTHORISED) from exc
            if response.status_code == 409:
                # The server is already being rebooted
                pass
            raise HostedPiException(str(exc)) from exc

        if wait:
            while self._info.is_booting:
                sleep(2)
            return self.power

    def cancel(self):
        """
        Cancel the Pi service
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-delete-piserversidentifier
        url = urllib.parse.urljoin(self._api_url, f"servers/{self.name}")
        response = self.session.delete(url)

        try:
            response.raise_for_status()
        except HTTPError as exc:
            if response.status_code == 403:
                raise HostedPiException(NOT_AUTHORISED) from exc
            raise HostedPiException(str(exc)) from exc

        self._cancelled = True

    def ssh_import_id(
        self,
        *,
        github: Union[set[str], list[str], None] = None,
        launchpad: Union[set[str], list[str], None] = None,
    ) -> set[str]:
        """
        Import SSH keys from GitHub or Launchpad, and add them to the Pi. Return the set of keys
        added.

        :type ssh_import_github: list or set or None
        :param ssh_import_github:
            A list/set of GitHub usernames to import SSH keys from (keyword-only argument)

        :type ssh_import_launchpad: list or set or None
        :param ssh_import_launchpad:
            A list/set of Launchpad usernames to import SSH keys from (keyword-only argument)
        """
        ssh_keys_set = parse_ssh_keys(
            ssh_import_github=github,
            ssh_import_launchpad=launchpad,
        )
        self.ssh_keys |= ssh_keys_set
        return ssh_keys_set
