from ipaddress import IPv6Address, IPv6Network
from time import sleep
from typing import Optional, Union, List, Set, TYPE_CHECKING

if TYPE_CHECKING:
    from .picloud import PiCloud

import requests
from requests.exceptions import HTTPError

from .utils import parse_ssh_keys
from .exc import HostedPiException


class Pi:
    """
    The ``Pi`` class represents a single Raspberry Pi service in the Mythic
    Beasts Pi cloud. Initialising a ``Pi`` object does not provision a new Pi,
    rather initialisation is for internal construction only.

    There are two ways to get access to a ``Pi`` object: retrieval from the
    :attr:`~hostedpi.picloud.PiCloud.pis` dictionary; and the return value of
    :meth:`~hostedpi.picloud.PiCloud.create_pi` method.

    With a ``Pi`` object, you can access data about that particular Pi service,
    add SSH keys, reboot it, cancel it and more.

    .. note::
        The ``Pi`` class should not be initialised by the user, only internally
        within the module.
    """
    def __init__(self, *, cloud: "PiCloud", name: str, model: int):
        self._cloud = cloud
        self._name = name
        self._model = model
        self._cancelled = False
        self._boot_progress = None
        self._disk_size = None
        self._initialised_keys = None
        self._ipv6_address = None
        self._ipv6_network = None
        self._is_booting = None
        self._location = None
        self._model_full = None
        self._power = None
        self._ipv4_ssh_port = None
        self._provision_status = None

    def __repr__(self):
        if self._cancelled:
            return f"<Pi {self.name} cancelled>"
        else:
            model = self.model_full if self.model_full else self.model
            return f"<Pi model {model} {self.name}>"

    def __str__(self):
        """
        A multi-line string of the information about the Pi
        """
        self._get_data()
        if self._provision_status == "live":
            if self._is_booting:
                boot_progress = "booting: {self._boot_progress}"
            elif self._boot_progress:
                boot_progress = self._boot_progress
            else:
                boot_progress = "live"
            num_keys = len(self.ssh_keys)
            power = "on" if self._power else "off"
            initialised_keys = "yes" if self._initialised_keys else "no"
            return f"""
Name: {self.name}
Provision status: {boot_progress}
Model: Raspberry Pi {self._model_full}
Disk size: {self._disk_size}GB
Power: {power}
IPv6 address: {self._ipv6_address}
IPv6 network: {self._ipv6_network}
Initialised keys: {initialised_keys}
SSH keys: {num_keys}
IPv4 SSH port: {self.ipv4_ssh_port}
Location: {self.location}
URLs:
  {self.url}
  {self.url_ssl}
SSH commands:
  {self.ipv4_ssh_command}  # IPv4
  {self.ipv6_ssh_command}  # IPv6
"""[1:-1]
        else:
            return f"""
Name: {self.name}
Provision status: {self._provision_status}
Model: Raspberry Pi {self._model}
Disk size: {self._disk_size}GB
IPv6 address: {self._ipv6_address}
IPv6 network: {self._ipv6_network}
SSH port: {self.ipv4_ssh_port}
Location: {self.location}
URLs:
  {self.url}
  {self.url_ssl}
SSH commands:
  {self.ipv4_ssh_command}  # IPv4
  {self.ipv6_ssh_command}  # IPv6
"""[1:-1]

    def _get_data(self):
        url = f"{self._API_URL}/{self.name}"
        r = requests.get(url, headers=self._cloud.headers)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise HostedPiException(e) from e

        data = r.json()
        self._boot_progress = data['boot_progress']
        disk_size = data.get('disk_size')
        if disk_size:
            self._disk_size = int(float(disk_size))
        self._initialised_keys = data['initialised_keys']
        self._ipv4_ssh_port = int(data['ssh_port'])
        self._ipv6_address = IPv6Address(data['ip'])
        self._ipv6_network = IPv6Network(data['ip_routed'])
        self._is_booting = bool(data['is_booting'])
        self._location = data['location']
        self._model = int(data['model'])
        self._model_full = data['model_full']
        self._power = bool(data['power'])
        self._provision_status = data['status']

    @property
    def _API_URL(self) -> str:
        return self._cloud._API_URL + '/servers'

    @property
    def name(self) -> str:
        """
        The name of the Pi service
        """
        return self._name

    @property
    def boot_progress(self) -> str:
        """
        A string representing the Pi's boot progress. Can be ``booted``,
        ``powered off`` or a particular stage of the boot process if currently
        booting.
        """
        self._get_data()
        if self._boot_progress:
            return self._boot_progress
        return "booted" if self.power else "powered off"

    @property
    def disk_size(self) -> int:
        """
        The Pi's disk size in GB
        """
        if self._disk_size is None:
            self._get_data()
        return self._disk_size

    @property
    def initialised_keys(self) -> bool:
        """
        A boolean representing whether or not the Pi has been initialised with
        SSH keys
        """
        self._get_data()
        return self._initialised_keys

    @property
    def ipv4_ssh_port(self) -> int:
        """
        The SSH port to use when connecting via the IPv4 proxy
        """
        if self._ipv4_ssh_port is None:
            self._get_data()
        return self._ipv4_ssh_port

    @property
    def ipv6_address(self) -> IPv6Address:
        """
        The Pi's IPv6 address as an :class:`~ipaddress.IPv6Address` object
        """
        if self._ipv6_address is None:
            self._get_data()
        return self._ipv6_address

    @property
    def ipv6_network(self) -> IPv6Network:
        """
        The Pi's IPv6 network as an :class:`~ipaddress.IPv6Network` object
        """
        if self._ipv6_network is None:
            self._get_data()
        return self._ipv6_network

    @property
    def is_booting(self) -> bool:
        """
        A boolean representing whether or not the Pi is currently booting
        """
        self._get_data()
        return self._is_booting

    @property
    def location(self) -> str:
        """
        The Pi's physical location (data centre)
        """
        if self._location is None:
            self._get_data()
        return self._location

    @property
    def model(self) -> int:
        """
        The Pi's model (3 or 4)
        """
        return self._model

    @property
    def model_full(self) -> str:
        """
        The Pi's model name (3B, 3B+ or 4B)
        """
        return self._model_full

    @property
    def power(self) -> bool:
        """
        A boolean representing whether or not the Pi is currently powered on
        """
        self._get_data()
        return self._power

    @property
    def provision_status(self) -> str:
        """
        A string representing the provision status of the Pi. Can be
        "provisioning", "initialising" or "live".
        """
        self._get_data()
        return self._provision_status

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
        A string containing the IPv4 SSH config for the Pi. The contents could
        be added to an SSH config file for easy access to the Pi.
        """
        return f"""Host {self.name}
    user root
    port {self.ipv4_ssh_port}
    hostname ssh.{self.name}.hostedpi.com
        """.strip()

    @property
    def ipv6_ssh_config(self) -> str:
        """
        A string containing the IPv6 SSH config for the Pi. The contents could
        be added to an SSH config file for easy access to the Pi.
        """
        return f"""Host {self.name}
    user root
    hostname {self.ipv6_address}
        """.strip()

    @property
    def ssh_keys(self) -> Set[str]:
        """
        Retrieve the SSH keys on the Pi, or use assignment to update them.
        Property value is a set of strings. Assigned value should also be a set
        of strings.
        """
        url = f"{self._API_URL}/{self.name}/ssh-key"
        r = requests.get(url, headers=self._cloud.headers)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise HostedPiException(e) from e

        body = r.json()

        keys = body['ssh_key']
        return {key.strip() for key in keys.split('\n') if key.strip()}

    @ssh_keys.setter
    def ssh_keys(self, ssh_keys: Union[Set[str], List[str]]):
        url = f"{self._API_URL}/{self.name}/ssh-key"
        headers = self._cloud.headers.copy()
        headers['Content-Type'] = 'application/json'
        if ssh_keys:
            ssh_keys_str = '\r\n'.join(set(ssh_keys))
        else:
            ssh_keys_str = '\r\n'  # server doesn't allow empty string
        data = {
            'ssh_key': ssh_keys_str,
        }

        r = requests.put(url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except HTTPError as e:
            if r.status_code == 403:
                raise HostedPiException("Not authorised to access server or server does not exist") from e
            raise HostedPiException(e) from e

    @property
    def url(self) -> str:
        """
        The http version of the hostedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser.
        """
        return f"http://www.{self.name}.hostedpi.com"

    @property
    def url_ssl(self) -> str:
        """
        The https version of the hostedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser, and an SSL certificate must be created.
            See https://letsencrypt.org/
        """
        return f"https://www.{self.name}.hostedpi.com"

    def _power_on_off(self, *, on=False):
        url = f"{self._API_URL}/{self.name}/power"
        data = {
            'power': on,
        }
        r = requests.put(url, headers=self._cloud.headers, json=data)

        try:
            r.raise_for_status()
        except HTTPError as e:
            if r.status_code == 403:
                raise HostedPiException("Not authorised to access server or server does not exist") from e
            raise HostedPiException(e) from e

    def on(self, *, wait: bool = False) -> Optional[bool]:
        """
        Power the Pi on. If *wait* is ``False`` (the default), return
        immediately. If *wait* is ``True``, wait until the power on request is
        completed, and return ``True`` on success, and ``False`` on failure.
        """
        self._power_on_off(on=True)
        if wait:
            while self.is_booting:
                sleep(2)
            return self.power

    def off(self):
        """
        Power the Pi off and return immediately
        """
        self._power_on_off(on=False)

    def reboot(self, *, wait: bool = False):
        """
        Reboot the Pi. If *wait* is ``False`` (the default), return ``None``
        immediately. If *wait* is ``True``, wait until the reboot request is
        completed, and return ``True`` on success, and ``False`` on failure.

        .. note::
            Note that if *wait* is ``False``, you can poll for the boot status
            while rebooting by inspecting the properties
            :attr:`~hostedpi.pi.Pi.is_booting` and
            :attr:`~hostedpi.pi.Pi.boot_progress`.
        """
        url = f"{self._API_URL}/{self.name}/reboot"
        r = requests.post(url, headers=self._cloud.headers)

        try:
            r.raise_for_status()
        except HTTPError as e:
            if r.status_code == 403:
                raise HostedPiException("Not authorised to access server or server does not exist") from e
            if r.status_code == 409:
                # The server is already being rebooted
                pass
            raise HostedPiException(e) from e

        if wait:
            while self.is_booting:
                sleep(2)
            return self.power

    def cancel(self):
        """
        Cancel the Pi service
        """
        url = f"{self._API_URL}/{self.name}"
        r = requests.delete(url, headers=self._cloud.headers)

        try:
            r.raise_for_status()
        except HTTPError as e:
            if r.status_code == 403:
                raise HostedPiException("Not authorised to access server or server does not exist") from e
            raise HostedPiException(e) from e

        self._cancelled = True

    def ssh_import_id(
        self,
        *,
        github: Optional[Union[Set[str], List[str]]] = None,
        launchpad: Optional[Union[Set[str], List[str]]] = None
    ) -> Set[str]:
        """
        Import SSH keys from GitHub or Launchpad, and add them to the Pi. Return
        the set of keys added.

        :type ssh_import_github: list or set or None
        :param ssh_import_github:
            A list/set of GitHub usernames to import SSH keys from (keyword-only
            argument)

        :type ssh_import_launchpad: list or set or None
        :param ssh_import_launchpad:
            A list/set of Launchpad usernames to import SSH keys from
            (keyword-only argument)
        """
        ssh_keys_set = parse_ssh_keys(
            ssh_import_github=github,
            ssh_import_launchpad=launchpad,
        )
        self.ssh_keys |= ssh_keys_set
        return ssh_keys_set
