from datetime import datetime, timedelta

import requests
from requests.exceptions import RequestException

from .exc import HostedPiException


class MythicAuth:
    _LOGIN_URL = 'https://auth.mythic-beasts.com/login'

    def __init__(self, api_id, secret):
        self._creds = (api_id, secret)
        self._token_expiry = datetime.now()
        self._authenticate()

    def __repr__(self):
        return '<MythicAuth>'

    @property
    def token(self):
        if datetime.now() > self._token_expiry:
            self._token = self._authenticate()
        return self._token

    def _authenticate(self):
        data = {
            'grant_type': 'client_credentials'
        }
        try:
            r = requests.post(self._LOGIN_URL, auth=self._creds, data=data)
        except RequestException as e:
            raise HostedPiException(str(e))

        body = r.json()

        if 'access_token' in body:
            self._token = body['access_token']
            self._token_expiry = datetime.now() + timedelta(seconds=body['expires_in'])
            return body['access_token']
        elif 'error_description' in body:
            raise HostedPiException(body['error_description'])
