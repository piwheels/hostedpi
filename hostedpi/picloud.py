import os
import string
from typing import Optional, Union, Dict, List, Set

from requests import Session, HTTPError

from .auth import MythicAuth
from .pi import Pi
from .utils import parse_ssh_keys
from .exc import HostedPiException


class PiCloud:
    """
    A connection to the Mythic Beasts Pi Cloud API for creating and managing
    cloud Pi services.

    Set up API keys at https://www.mythic-beasts.com/customer/api-users

    :type api_id: str or None
    :param api_id:
        Your Mythic Beasts API ID (alternatively, the environment variable
        ``HOSTEDPI_ID`` can be used)

    :type api_secret: str or None
    :param api_secret:
        Your Mythic Beasts API secret (alternatively, the environment variable
        ``HOSTEDPI_SECRET`` can be used)

    :type ssh_keys: list or set or None
    :param ssh_keys:
        A list/set of SSH key strings (keyword-only argument)

    :type ssh_key_path: str or None
    :param ssh_key_path:
        The path to your SSH public key (keyword-only argument)

    :type ssh_import_github: list or set or None
    :param ssh_import_github:
        A list/set of GitHub usernames to import SSH keys from (keyword-only
        argument)

    :type ssh_import_launchpad: list or set or None
    :param ssh_import_launchpad:
        A list/set of Launchpad usernames to import SSH keys from (keyword-only
        argument)

    .. note::
        If any SSH keys are provided on class initialisation, they will be used
        when creating Pis but are overriden by any passed to the
        :meth:`~hostedpi.picloud.PiCloud.create_pi` method.

        All SSH arguments provided will be used in combination.
    """

    _API_URL = "https://api.mythic-beasts.com/beta/pi"

    def __init__(
        self,
        api_id: Optional[str] = None,
        api_secret: Optional[str] = None,
        *,
        ssh_keys: Optional[Union[List[str], Set[str]]] = None,
        ssh_key_path: Optional[str] = None,
        ssh_import_github: Optional[Union[List[str], Set[str]]] = None,
        ssh_import_launchpad: Optional[Union[List[str], Set[str]]] = None,
    ):
        if api_id is None:
            api_id = os.environ.get("HOSTEDPI_ID")

        if api_secret is None:
            api_secret = os.environ.get("HOSTEDPI_SECRET")

        if api_id is None or api_secret is None:
            raise HostedPiException(
                "Environment variables HOSTEDPI_ID and HOSTEDPI_SECRET must be "
                "set or api_id and api_secret passed as arguments"
            )

        self.ssh_keys = parse_ssh_keys(
            ssh_keys, ssh_key_path, ssh_import_github, ssh_import_launchpad
        )

        self._auth = MythicAuth(api_id, api_secret)

    def __repr__(self):
        return "<PiCloud>"

    def __str__(self):
        """
        String of information about all the Pis in the account
        """
        print(*self.pis, sep="\n\n")

    @property
    def session(self) -> Session:
        return self._auth.session

    @property
    def pis(self) -> Dict[str, Pi]:
        """
        A dictionary of :class:`~hostedpi.pi.Pi` objects keyed by their names
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piservers
        url = f"{self._API_URL}/servers"
        r = self.session.get(url)

        try:
            r.raise_for_status()
        except HTTPError as e:
            if r.status_code == 403:
                raise HostedPiException("Not authorised") from e
            raise HostedPiException(e) from e

        pis = r.json()["servers"]

        return {
            name: Pi(cloud=self, name=name, model=data["model"])
            for name, data in sorted(pis.items())
        }

    @property
    def ipv4_ssh_config(self) -> str:
        """
        A string containing the IPv4 SSH config for all Pis within the account.
        The contents could be added to an SSH config file for easy access to the
        Pis in the account.
        """
        return "\n".join(pi.ipv4_ssh_config for pi in self.pis.values())

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
        name: str,
        *,
        model: int = 3,
        disk_size: int = 10,
        os_image: Optional[str] = None,
        ssh_keys: Optional[Union[List[str], Set[str]]] = None,
        ssh_key_path: Optional[str] = None,
        ssh_import_github: Optional[Union[List[str], Set[str]]] = None,
        ssh_import_launchpad: Optional[Union[List[str], Set[str]]] = None,
    ) -> Pi:
        """
        Provision a new cloud Pi with the specified name, model, disk size and
        SSH keys. Return a new :class:`~hostedpi.pi.Pi` instance.

        :type name: str
        :param name:
            A unique identifier for the server. This will form part of the
            hostname for the server, and must consist only of alphanumeric
            characters and hyphens.

        :type model: int or None
        :param model:
            The Raspberry Pi model to provision (3 or 4) - defaults to 3
            (keyword-only argument)

        :type disk_size: int or None
        :param disk_size:
            The amount of disk space (in GB) attached to the Pi - must be a
            multiple of 10 - defaults to 10 (keyword-only argument)

        :type os_image: str
        :param os_image:
            The name of the operating system image to boot from. Defaults to
            ``None`` which falls back to Mythic's default (Raspbian/PiOS
            stable). If given, this must be a string which appears as a key in
            the return value of
            :meth:`~hostedpi.picloud.PiCloud.get_operating_systems` for the
            relevant Pi model.

        :type ssh_keys: list or set or None
        :param ssh_keys:
            A list/set of SSH key strings (keyword-only argument)

        :type ssh_key_path: str or None
        :param ssh_key_path:
            The path to your SSH public key (keyword-only argument)

        :type ssh_import_github: list or set or None
        :param ssh_import_github:
            A list/set of GitHub usernames to import SSH keys from (keyword-only
            argument)

        :type ssh_import_launchpad: list or set or None
        :param ssh_import_launchpad:
            A list/set of Launchpad usernames to import SSH keys from
            (keyword-only argument)

        .. note::
            If any SSH keys are provided on class initialisation, they will be
            used here but are overriden by any passed to this method.

        .. note::
            When requesting a Pi 3, you will either get a model 3B or 3B+. It is
            not possible to request a particular model beyond 3 or 4. The Pi 4
            is the 4GB RAM model.
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-post-piserversidentifier
        ssh_keys_set = parse_ssh_keys(
            ssh_keys, ssh_key_path, ssh_import_github, ssh_import_launchpad
        )
        ssh_keys_str = "\r\n".join(ssh_keys_set)

        server_name = name.lower()
        self._validate_server_name(server_name)
        self._validate_model(model)
        self._validate_disk_size(disk_size)

        url = f"{self._API_URL}/servers/{name}"
        data = {
            "disk": disk_size,
            "model": model,
            "os_image": os_image,
        }

        if ssh_keys:
            data["ssh_key"] = ssh_keys_str

        r = self.session.post(url, json=data)

        try:
            r.raise_for_status()
        except HTTPError as e:
            if r.status_code == 400:
                error = r.json().get("error", "")
                raise HostedPiException(f"Invalid parameters: {error}") from e
            if r.status_code == 403:
                raise HostedPiException("Not authorised to provision server") from e
            if r.status_code == 409:
                raise HostedPiException("Server name already exists") from e
            if r.status_code == 503:
                raise HostedPiException(f"Out of stock of Pi Model {model}") from e
            raise HostedPiException(e) from e

        return Pi(cloud=self, name=name, model=model)

    def _validate_server_name(self, server_name):
        valid_chars = string.ascii_lowercase + string.digits + "-_"
        if not all(c in valid_chars for c in server_name):
            raise HostedPiException(
                "Server name must consist of alphanumeric characters and " "hyphens"
            )

    def _validate_model(self, model: int):
        if model not in {3, 4}:
            raise HostedPiException("Model must be 3 or 4")

    def _validate_disk_size(self, disk_size: int):
        if disk_size < 10 or disk_size % 10 > 0:
            raise HostedPiException("Disk size must be a multiple of 10")

    def get_operating_systems(self, *, model: int) -> Dict[str, str]:
        """
        Return a dict of operating systems supported by the given Pi *model* (3
        or 4). Dict keys are identifiers (e.g. "rpi-buster-armhf") which can be
        used when provisioning a new Pi with
        :meth:`~hostedpi.picloud.PiCloud.create_pi`; dict values are text labels
        of the OS/distro names (e.g. "Raspberry Pi OS Bullseye (32 bit)").

        :type model: int
        :param model:
            The Raspberry Pi model (3 or 4) to get operating systems for
            (keyword-only argument)
        """
        # https://www.mythic-beasts.com/support/api/raspberry-pi#ep-get-piimagesmodel
        if model not in {3, 4}:
            raise HostedPiException("model must be 3 or 4")
        url = f"{self._API_URL}/images/{model}"
        r = self.session.get(url)

        try:
            r.raise_for_status()
        except HTTPError as e:
            if r.status_code == 400:
                error = r.json()["error"]
                raise HostedPiException(error) from e
            raise HostedPiException(e) from e

        return r.json()
