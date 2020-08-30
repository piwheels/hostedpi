from datetime import datetime, timedelta

import requests
from requests.exceptions import RequestException

from .exc import HostedPiException


class MythicAuth:
    _LOGIN_URL = 'https://auth.mythic-beasts.com/login'

    def __init__(self, username, password):
        self.creds = (username, password)
        self._token = None
        self._token_expiry = datetime.now()

    def __repr__(self):
        return '<hostedpi.MythicAuth>'

    @property
    def token(self):
        if datetime.now() > self._token_expiry:
            self._token = self.authenticate()
        return self._token

    def authenticate(self):
        data = {
            'grant_type': 'client_credentials'
        }
        try:
            r = requests.post(self._LOGIN_URL, auth=self.creds, data=data)
        except RequestException as e:
            raise HostedPiException(str(e))
        body = r.json()
        self._token = body['access_token']
        self._token_expiry = datetime.now() + timedelta(seconds=body['expires_in'])
        return body['access_token']
