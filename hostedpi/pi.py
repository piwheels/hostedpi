from datetime import datetime, timedelta
import webbrowser
import io
import os
import subprocess
import json

import requests

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
    def __init__(self, *, parent, name, model):
        self._parent = parent
        self._name = name
        self._model = model
        self._cancelled = False
        self._cached_data = None

    def __repr__(self):
        if self._cancelled:
            return '<Pi {} cancelled>'.format(self.name)
        else:
            return '<Pi model {} {}>'.format(self.model, self.name)

    @property
    def name(self):
        "The Pi's server name."
        return self._name

    @property
    def model(self):
        "The Pi's model (3 or 4)."
        return self._model

    @property
    def data(self):
        "A dictionary of the Pi's data."
        url = '{}/{}'.format(self._parent._API_URL, self.name)
        try:
            r = requests.get(url, headers=self._parent._headers)
        except RequestException as e:
            raise HostedPiException(str(e))

        if r.ok:
            data = r.json()
        else:
            raise HostedPiException('{}: {}'.format(r.status_code, r.reason))

        self._cached_data = data

        return data

    @property
    def cached_data(self):
        """
        The last retrieved data to save making an API request. If the data has
        not yet been looked up, an API request will be made.
        """
        if self._cached_data is None:
            self._cached_data = self.data

        return self._cached_data

    @property
    def disk_size(self):
        """
        The Pi's disk size (this value will not change so the result is
        cached).
        """
        return self.cached_data['disk_size']

    @property
    def ssh_port(self):
        """
        The Pi's SSH port (this value will not change so the result is
        cached).
        """
        return self.cached_data['ssh_port']

    @property
    def ip(self):
        """
        The Pi's IPv6 address (this value will not change so the result is
        cached).
        """
        return self.cached_data['ip']

    @property
    def ip_routed(self):
        """
        The Pi's routed IPv6 address (this value will not change so the result
        is cached).
        """
        return self.cached_data['ip_routed']

    @property
    def location(self):
        """
        The Pi's physical location (data centre) (this value will not change so
        the result is cached).
        """
        return self.cached_data['location']

    @property
    def status(self):
        """
        A string representing the provision status of the Pi. Can be either
        "initialising" or "live".
        """
        return self.data['status']

    @property
    def initialised_keys(self):
        """
        A boolean representing whether or not the Pi has been initialised with
        SSH keys.
        """
        return self.data['initialised_keys']

    @property
    def power(self):
        """
        A boolean representing whether or not the Pi is currently powered on.
        """
        return self.data['power']

    @property
    def ssh_command(self):
        "The SSH command required to connect to the Pi."
        return 'ssh -p {} root@ssh.{}.hostedpi.com'.format(self.ssh_port, self.name)

    @property
    def ssh_config(self):
        """
        A string containing the SSH config for the Pi. The contents could be
        added to an SSH config file for easy access to the Pi.
        """
        return """Host {0}
    user root
    port {1}
    hostname ssh.{0}.hostedpi.com
        """.format(self.name, self.ssh_port).strip()

    @property
    def ssh_keys(self):
        """
        Retrieve the list of SSH keys on the Pi, or use assignment to update
        them. Property value is a list of strings. Assigned value should also be
        a list of strings.
        """
        url = '{}/{}/ssh-key'.format(self._parent._API_URL, self.name)
        r = requests.get(url, headers=self._parent._headers)

        if r.ok:
            body = r.json()
        else:
            raise HostedPiException('{}: {}'.format(r.status_code, r.reason))

        keys = body['ssh_key']
        return keys.split('\r\n')

    @ssh_keys.setter
    def ssh_keys(self, ssh_keys):
        url = '{}/{}/ssh-key'.format(self._parent._API_URL, self.name)
        headers = self._parent._headers.copy()
        headers['Content-Type'] = 'application/json'
        ssh_keys_str = '\r\n'.join(ssh_keys)
        data = {
            'ssh_key': ssh_keys_str,
        }

        r = requests.put(url, headers=headers, json=data)
        if not r.ok:
            raise HostedPiException('{}: {}'.format(r.status_code, r.reason))

    @property
    def url(self):
        """
        The http version of the hopstedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser.
        """
        return 'http://www.{}.hostedpi.com'.format(self.name)

    @property
    def url_ssl(self):
        """
        The https version of the hopstedpi.com URL of the Pi.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser, and an SSL certificate must be created.
            See https://letsencrypt.org/
        """
        return 'https://www.{}.hostedpi.com'.format(self.name)

    def reboot(self):
        "Reboot the Pi."
        url = '{}/{}/reboot'.format(self._parent._API_URL, self.name)
        r = requests.post(url, headers=self._parent._headers)
        if r.ok:
            body = r.json()
        elif 'error' in body:
            raise HostedPiException(body['error'])
        else:
            raise HostedPiException('{}: {}'.format(r.status_code, r.reason))

    def cancel(self):
        "Cancel the Pi service."
        url = '{}/{}'.format(self._parent._API_URL, self.name)
        r = requests.delete(url, headers=self._parent._headers)
        if r.ok:
            body = r.json()
            if 'error' in body:
                raise HostedPiException(body['error'])
            else:
                self._cancelled = True
        else:
            raise HostedPiException('{}: {}'.format(r.status_code, r.reason))

    def open_web(self, *, ssl=False):
        """
        Open the Pi's web address in the default browser. Use https if *ssl* is
        True.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser, and an SSL certificate must be created for
            the https URL to resolve. See https://letsencrypt.org/
        """
        url = self.url_ssl if ssl else self.url
        webbrowser.open(url)

    def ping_ipv6(self):
        """
        Ping the Pi's IPv6 address and return True if successful.

        ..note::
            Note this requires IPv6 connectivity
        """
        # note this only works if you have IPv6
        with io.open(os.devnull, 'wb') as devnull:
            try:
                subprocess.check_call(
                    ['ping', '-c1', host],
                    stdout=devnull, stderr=devnull)
            except subprocess.CalledProcessError:
                return False
            else:
                return True

    def get_web(self, *, ssl=False):
        """
        Send a GET request to the Pi's web address, and return True if a
        successful request was made. Use https if *ssl* is True.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser, and an SSL certificate must be created for
            the https URL to resolve. See https://letsencrypt.org/
        """
        url = self.url_ssl if ssl else self.url
        r = requests.get(url)
        return r.ok

    def get_web_contents(self, *, ssl=False):
        """
        Send a GET request to the Pi's web address, and return True if a
        successful request was made. Use https if *ssl* is True.

        .. note::
            Note that a web server must be installed on the Pi for the URL to
            resolve in a web browser, and an SSL certificate must be created for
            the https URL to resolve. See https://letsencrypt.org/
        """
        url = self.url_ssl if ssl else self.url
        r = requests.get(url)
        return r.text
