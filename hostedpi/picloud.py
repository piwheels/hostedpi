from pathlib import Path
from datetime import datetime, timedelta

import requests
from requests.exceptions import RequestException

from .auth import MythicAuth
from .pi import Pi
from .exc import HostedPiException


class PiCloud:
    _API_URL = 'https://api.mythic-beasts.com/beta/servers/pi'

    def __init__(self, username, password, ssh_keys=None, ssh_keys_path=None):
        self._username = username
        self._auth = MythicAuth(username, password)
        if ssh_keys:
            self.ssh_keys = ssh_keys
        elif ssh_keys_path:
            self.ssh_keys = self._read_ssh_keys(ssh_keys_path)
        else:
            self.ssh_keys = None
        self._next_status_check = datetime.now()

    def __repr__(self):
        return f'<PiCloud {self.username}>'

    @property
    def _headers(self):
        return {
            'Authorization': f'Bearer {self._auth.token}',
        }

    @property
    def username(self):
        return self._username

    @property
    def cache_is_invalid(self):
        return datetime.now() > self._next_status_check

    @property
    def pis(self):
        if self.cache_is_invalid:
            try:
                r = requests.get(self._API_URL, headers=self._headers)
            except RequestException as e:
                raise HostedPiException(str(e))
            pis = r.json()['servers']
            self._pis = {
                name: Pi(parent=self, name=name, model=data['model'])
                for name, data in pis.items()
            }
            self._next_status_check = datetime.now() + timedelta(minutes=1)
        return self._pis

    def _read_ssh_keys(self, ssh_keys_path):
        with open(ssh_keys_path) as f:
            return f.read()

    def create_pi(self, name, model=3, disk=10, ssh_keys=None, ssh_keys_path=None):
        url = f'{self._API_URL}/{name}'
        data = {
            'disk': disk,
            'model': model,
        }

        try:
            r = requests.post(url, headers=self._headers, json=data)
        except RequestException as e:
            raise HostedPiException(str(e))
        body = r.json()
        if 'error' in body:
            raise HostedPiException(body['error'])
        pi = Pi(parent=self, name=name, model=model)
        self._pis[name] = pi
        return pi
