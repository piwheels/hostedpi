from datetime import datetime, timedelta
import webbrowser
import io
import os
import subprocess
import json
from ipaddress import IPv6Address, IPv6Network
from threading import Thread

import requests
from requests.exceptions import RequestException

from .utils import ssh_import_id, parse_ssh_keys
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
        self._status = None
        self._data_expiry = datetime.now()
        self._reboot_thread = None

    def __repr__(self):
        if self._cancelled:
            return "<Pi {} cancelled>".format(self.name)
        else:
            model = self.model_full if self.model_full else self.model
            return "<Pi model {} {}>".format(model, self.name)

    def _get_data(self):
        url = "{}/{}".format(self._cloud._API_URL, self.name)
        try:
            r = requests.get(url, headers=self._cloud.headers)
        except RequestException as e:
            raise HostedPiException(str(e))

        if r.ok:
            data = r.json()
        else:
            raise HostedPiException("{}: {}".format(r.status_code, r.reason))

        self._boot_progress = data['boot_progress']
        self._disk_size = int(float(data['disk_size']))
        self._initialised_keys = data['initialised_keys']
        self._ipv4_ssh_port = int(data['ssh_port'])
        self._ipv6_address = IPv6Address(data['ip'])
        self._ipv6_network = IPv6Network(data['ip_routed'])
        self._is_booting = bool(data['is_booting'])
        self._location = data['location']
        self._model = int(data['model'])
        self._model_full = data['model_full']
        self._power = bool(data['power'])
        self._status = data['status']

    @property
    def name(self):
        "The name of the Pi service."
        return self._name

    @property
    def boot_progress(self):
        """
        The Pi's boot progress. ``None`` if booted successfully, otherwise will
        be a string.
        """
        self._get_data()
        return self._boot_progress

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
        The Pi's IPv6 address.
        """
        if self._ipv6_address is None:
            self._get_data()
        return self._ipv6_address

    @property
    def ipv6_network(self):
        """
        The Pi's IPv6 network.
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
    def status(self):
        """
        A string representing the provision status of the Pi. Can be
        "provisioning", "initialising" or "live".
        """
        self._get_data()
        return self._status

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
        url = "{}/{}/ssh-key".format(self._cloud._API_URL, self.name)
        r = requests.get(url, headers=self._cloud.headers)

        if r.ok:
            body = r.json()
        else:
            raise HostedPiException("{}: {}".format(r.status_code, r.reason))

        keys = body['ssh_key']
        return {key.strip() for key in keys.split("\n") if key.strip()}

    @ssh_keys.setter
    def ssh_keys(self, ssh_keys):
        url = "{}/{}/ssh-key".format(self._cloud._API_URL, self.name)
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
        if not r.ok:
            raise HostedPiException("{}: {}".format(r.status_code, r.reason))

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

    def reboot(self, *, wait=False):
        """
        Reboot the Pi. If *wait* is ``False`` (the default), return ``None``
        immediately. If *wait* is ``False``, wait until the reboot request is
        completed, and return ``True`` on success, and ``False`` on failure.

        .. note::
            Note that if *wait* is ``False``, you can poll for the boot status
            while rebooting by inspecting the properties
            :attr:`~hostedpi.pi.Pi.is_booting` and
            :attr:`~hostedpi.pi.Pi.boot_progress`.
        """
        def request_reboot():
            url = "{}/{}/reboot".format(self._cloud._API_URL, self.name)
            r = requests.post(url, headers=self._cloud.headers)
            return r
            if r.ok:
                return True
            else:
                return False
        if wait:
            return request_reboot()
        else:
            self._reboot_thread = Thread(target=request_reboot, daemon=True)
            self._reboot_thread.start()

    def cancel(self):
        "Cancel the Pi service."
        url = "{}/{}".format(self._cloud._API_URL, self.name)
        r = requests.delete(url, headers=self._cloud.headers)
        if r.ok:
            body = r.json()
            if 'error' in body:
                raise HostedPiException(body['error'])
            else:
                self._cancelled = True
        else:
            raise HostedPiException("{}: {}".format(r.status_code, r.reason))

    def ssh_import_id(self, *, github=None, launchpad=None):
        """
        Import SSH keys from GitHub or Launchpad, and add them to the Pi.

        :type ssh_import_github: list or set or None
        :param ssh_import_github:
            A list/set of GitHub usernames to import SSH keys from (keyword-only
            argument)

        :type ssh_import_launchpad: list or set or None
        :param ssh_import_launchpad:
            A list/set of Launchpad usernames to import SSH keys from
            (keyword-only argument)
        """
        ssh_keys_set = parse_ssh_keys(ssh_import_github=ssh_import_github,
                                      ssh_import_launchpad=ssh_import_launchpad)
        self.ssh_keys |= ssh_keys_set

    def pprint(self):
        "Pretty print the information about the Pi"
        self._get_data()
        num_keys = len(self.ssh_keys)
        if self._status == "live":
            if self._is_booting:
                boot_progress = "booting: {}".format(self._boot_progress)
            elif self._boot_progress:
                boot_progress = self._boot_progress
            else:
                boot_progress = "live"
            print("Name:", self.name)
            print("Status:", boot_progress)
            print("Model: Raspberry Pi", self._model_full)
            print("Disk size:", self._disk_size, "GB")
            print("Power:", "Yes" if self._power else "No")
            print("IPv6 address:", self._ipv6_address)
            print("IPv6 network:", self._ipv6_network)
            print("Initialised keys:", "Yes" if self._initialised_keys else "No")
            print("SSH keys:", num_keys)
            print("SSH port:", self.ipv4_ssh_port)
            print("Location:", self.location)
            print("URLs:")
            print(" ", self.url)
            print(" ", self.url_ssl)
            print("SSH commands:")
            print("  IPv4:", self.ipv4_ssh_command)
            print("  IPv6:", self.ipv6_ssh_command)
        else:
            print("Name:", self.name)
            print("Status:", self.status)
            print("Model: Raspberry Pi", self._model)
            print("Disk size:", self._disk_size, "GB")
            print("IPv6 address:", self._ipv6_address)
            print("IPv6 network:", self._ipv6_network)
            print("SSH port:", self.ipv4_ssh_port)
            print("Location:", self.location)
            print("URLs:")
            print(" ", self.url)
            print(" ", self.url_ssl)
            print("SSH commands:")
            print("  IPv4:", self.ipv4_ssh_command)
            print("  IPv6:", self.ipv6_ssh_command)
