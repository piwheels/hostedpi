import os
from pathlib import Path
from datetime import datetime, timedelta

import requests
from requests.exceptions import RequestException

from .auth import MythicAuth
from .pi import Pi
from .utils import ssh_import_id, parse_ssh_keys
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

        All SSH arguments provided will be used in combination
    """
    _API_URL = 'https://api.mythic-beasts.com/beta/servers/pi'

    def __init__(self, api_id=None, api_secret=None, *, ssh_keys=None,
                 ssh_key_path=None, ssh_import_github=None,
                 ssh_import_launchpad=None):
        if api_id is None:
            api_id = os.environ.get('HOSTEDPI_ID')

        if api_secret is None:
            api_secret = os.environ.get('HOSTEDPI_SECRET')

        if api_id is None or api_secret is None:
            raise HostedPiException(
                "Environment variables HOSTEDPI_ID and HOSTEDPI_SECRET must be "
                "set or api_id and api_secret passed as arguments"
            )

        self.ssh_keys = parse_ssh_keys(ssh_keys, ssh_key_path,
                                       ssh_import_github, ssh_import_launchpad)

        self._auth = MythicAuth(api_id, api_secret)

    def __repr__(self):
        return "<PiCloud>"

    @property
    def headers(self):
        return self._auth.headers

    @property
    def pis(self):
        "A dictionary of :class:`~hostedpi.pi.Pi` objects keyed by their names."
        try:
            r = requests.get(self._API_URL, headers=self.headers)
        except RequestException as e:
            raise HostedPiException(str(e))

        pis = r.json()['servers']

        return {
            name: Pi(cloud=self, name=name, model=data['model'])
            for name, data in sorted(pis.items())
        }

    @property
    def ipv4_ssh_config(self):
        """
        A string containing the IPv4 SSH config for all Pis within the account.
        The contents could be added to an SSH config file for easy access to the
        Pis in the account.
        """
        return "\n".join(pi.ipv4_ssh_config for pi in self.pis.values())

    @property
    def ipv6_ssh_config(self):
        """
        A string containing the IPv6 SSH config for all Pis within the account.
        The contents could be added to an SSH config file for easy access to the
        Pis in the account.
        """
        return "\n".join(pi.ipv6_ssh_config for pi in self.pis.values())

    def create_pi(self, name, *, model=3, disk_size=10, ssh_keys=None,
                  ssh_key_path=None, ssh_import_github=None,
                  ssh_import_launchpad=None):
        """
        Provision a new cloud Pi with the specified name, model, disk size and
        SSH keys. Return a new :class:`~hostedpi.pi.Pi` instance.

        :type name: str
        :param name:
            The name of the Pi service to create (must be unique)

        :type model: int
        :param model:
            The Raspberry Pi model to provision (3 or 4) - defaults to 3
            (keyword-only argument)

        :type disk_size: int
        :param disk_size:
            The amount of disk space (in GB) attached to the Pi - must be a
            multiple of 10 - defaults to 10 (keyword-only argument)

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
        ssh_keys_set = parse_ssh_keys(ssh_keys, ssh_key_path, ssh_import_github,
                                      ssh_import_launchpad)
        ssh_keys_str = "\r\n".join(ssh_keys_set)

        model = str(model)
        if model not in ('3', '4'):
            raise HostedPiException("model must be 3 or 4")

        if disk_size < 10 or disk_size % 10 > 0:
            raise HostedPiException("disk size must be a multiple of 10")

        url = '{}/{}'.format(self._API_URL, name)
        data = {
            'disk': disk_size,
            'model': model,
        }

        if ssh_keys:
            data['ssh_key'] = ssh_keys_str

        try:
            r = requests.post(url, headers=self.headers, json=data)
        except RequestException as e:
            raise HostedPiException(str(e))

        body = r.json()

        if 'error' in body:
            raise HostedPiException(body['error'])

        return Pi(cloud=self, name=name, model=model)

    def pprint(self):
        for pi in self.pis.values():
            pi.pprint()
            print()
