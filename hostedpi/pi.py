from datetime import datetime
from ipaddress import IPv6Address, IPv6Network
from time import sleep

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
    def __init__(self, *, cloud, name, model):
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
        self._data_expiry = datetime.now()
        self._reboot_thread = None

    def __repr__(self):
        if self._cancelled:
            return "<Pi {} cancelled>".format(self.name)
        else:
            model = self.model_full if self.model_full else self.model
            return "<Pi model {} {}>".format(model, self.name)

    def __str__(self):
        "A string of the information about the Pi"
        self._get_data()
        if self._provision_status == "live":
            if self._is_booting:
                boot_progress = "booting: {}".format(self._boot_progress)
            elif self._boot_progress:
                boot_progress = self._boot_progress
            else:
                boot_progress = "live"
            num_keys = len(self.ssh_keys)
            power = "on" if self._power else "off"
            initialised_keys = "yes" if self._initialised_keys else "no"
            return """
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
  IPv4: {self.ipv4_ssh_command}
  IPv6: {self.ipv6_ssh_command}
"""[1:-1].format(self=self, boot_progress=boot_progress, power=power,
                 num_keys=num_keys, initialised_keys=initialised_keys)
        else:
            return """
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
"""[1:-1].format(self=self)

    def _get_data(self):
        url = "{}/{}".format(self._API_URL, self.name)
        r = requests.get(url, headers=self._cloud.headers)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise HostedPiException(e)

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
        self._model = data['model']
        self._model_full = data['model_full']
        self._power = bool(data['power'])
        self._provision_status = data['status']

    @property
    def _API_URL(self):
        return self._cloud._API_URL + '/pi'

    @property
    def name(self):
        "The name of the Pi service."
        return self._name

    @property
    def boot_progress(self):
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
    def disk_size(self):
        """
        The Pi's disk size in GB.
        """
        if self._disk_size is None:
            self._get_data()
        return self._disk_size

    @property
    def initialised_keys(self):
        """
        A boolean representing whether or not the Pi has been initialised with
        SSH keys.
        """
        self._get_data()
        return self._initialised_keys

    @property
    def ipv4_ssh_port(self):
        "The SSH port to use when connecting via the IPv4 proxy."
        if self._ipv4_ssh_port is None:
            self._get_data()
        return self._ipv4_ssh_port

    @property
    def ipv6_address(self):
        """
        The Pi's IPv6 address as an :class:`~ipaddress.IPv6Address` object.
        """
        if self._ipv6_address is None:
            self._get_data()
        return self._ipv6_address

    @property
    def ipv6_network(self):
        """
        The Pi's IPv6 network as an :class:`~ipaddress.IPv6Network` object.
        """
        if self._ipv6_network is None:
            self._get_data()
        return self._ipv6_network

    @property
    def is_booting(self):
        "A boolean representing whether or not the Pi is currently booting."
        self._get_data()
        return self._is_booting

    @property
    def location(self):
        """
        The Pi's physical location (data centre).
        """
        if self._location is None:
            self._get_data()
        return self._location

    @property
    def model(self):
        "The Pi's model (3 or 4)."
        return self._model

    @property
    def model_full(self):
        "The Pi's model (3 or 4)."
        return self._model_full

    @property
    def power(self):
        """
        A boolean representing whether or not the Pi is currently powered on.
        """
        self._get_data()
        return self._power

    @property
    def provision_status(self):
        """
        A string representing the provision status of the Pi. Can be
        "provisioning", "initialising" or "live".
        """
        self._get_data()
        return self._provision_status

    @property
    def ipv4_ssh_command(self):
        "The SSH command required to connect to the Pi over IPv4."
        return "ssh -p {} root@ssh.{}.hostedpi.com".format(self.ipv4_ssh_port,
                                                           self.name)

    @property
    def ipv6_ssh_command(self):
        "The SSH command required to connect to the Pi over IPv6."
        return "ssh root@[{}]".format(self.ipv6_address)

    @property
    def ipv4_ssh_config(self):
        """
        A string containing the IPv4 SSH config for the Pi. The contents could
        be added to an SSH config file for easy access to the Pi.
        """
        return """Host {0}
    user root
    port {1}
    hostname ssh.{0}.hostedpi.com
        """.format(self.name, self.ipv4_ssh_port).strip()

    @property
    def ipv6_ssh_config(self):
        """
        A string containing the IPv6 SSH config for the Pi. The contents could
        be added to an SSH config file for easy access to the Pi.
        """
        return """Host {0}
    user root
    hostname {1}
        """.format(self.name, self.ipv6_address).strip()

    @property
    def ssh_keys(self):
        """
        Retrieve the SSH keys on the Pi, or use assignment to update them.
        Property value is a set of strings. Assigned value should also be a set
        of strings.
        """
        url = "{}/{}/ssh-key".format(self._API_URL, self.name)
        r = requests.get(url, headers=self._cloud.headers)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise HostedPiException(e)

        body = r.json()

        keys = body['ssh_key']
        return {key.strip() for key in keys.split("\n") if key.strip()}

    @ssh_keys.setter
    def ssh_keys(self, ssh_keys):
        url = "{}/{}/ssh-key".format(self._API_URL, self.name)
        headers = self._cloud.headers.copy()
        headers['Content-Type'] = 'application/json'
        if ssh_keys:
            ssh_keys_str = "\r\n".join(set(ssh_keys))
        else:
            ssh_keys_str = "\r\n"  # hack: server doesn't allow empty string
        data = {
            'ssh_key': ssh_keys_str,
        }

        r = requests.put(url, headers=headers, json=data)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise HostedPiException(e)

    @property
    def url(self):
        """
        The http version of the hostedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser.
        """
        return "http://www.{}.hostedpi.com".format(self.name)

    @property
    def url_ssl(self):
        """
        The https version of the hostedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser, and an SSL certificate must be created.
            See https://letsencrypt.org/
        """
        return "https://www.{}.hostedpi.com".format(self.name)

    def _power_on_off(self, *, on=False):
        url = "{}/{}/power".format(self._API_URL, self.name)
        data = {
            'power': on,
        }
        r = requests.put(url, headers=self._cloud.headers, json=data)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise HostedPiException(e)

    def on(self, *, wait=False):
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
        Power the Pi off and return immediately.
        """
        self._power_on_off(on=False)

    def reboot(self, *, wait=False):
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
        url = "{}/{}/reboot".format(self._API_URL, self.name)
        r = requests.post(url, headers=self._cloud.headers)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise HostedPiException(e)

        if wait:
            while self.is_booting:
                sleep(2)
            return self.power

    def cancel(self):
        "Cancel the Pi service."
        url = "{}/{}".format(self._API_URL, self.name)
        r = requests.delete(url, headers=self._cloud.headers)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise HostedPiException(e)

        body = r.json()
        self._cancelled = True

    def ssh_import_id(self, *, github=None, launchpad=None):
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
        ssh_keys_set = parse_ssh_keys(ssh_import_github=github,
                                      ssh_import_launchpad=launchpad)
        self.ssh_keys |= ssh_keys_set
        return ssh_keys_set
