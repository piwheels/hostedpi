from datetime import datetime, timedelta

import requests
from requests.exceptions import HTTPError

from .exc import MythicAuthenticationError
from .__version__ import __version__


class MythicAuth:
    _LOGIN_URL = "https://auth.mythic-beasts.com/login"

    def __init__(self, api_id, api_secret):
        self._creds = (api_id, api_secret)
        self._token = None
        self._token_expiry = datetime.now()
        self._headers = {
            'User-Agent': 'python-hostedpi/' + __version__,
        }
        self._authenticate()

    def __repr__(self):
        return "<MythicAuth>"

    @property
    def headers(self):
        headers = self._headers
        headers['Authorization'] = 'Bearer ' + self.token
        return headers

    @property
    def token(self):
        if datetime.now() > self._token_expiry:
            self._token = self._authenticate()
        return self._token

    def _authenticate(self):
        data = {
            'grant_type': 'client_credentials'
        }
        r = requests.post(self._LOGIN_URL, headers=self._headers,
                          auth=self._creds, data=data)

        try:
            r.raise_for_status()
        except HTTPError as e:
            raise MythicAuthenticationError("Failed to authenticate") from e

        body = r.json()
        if 'access_token' in body:
            self._token = body['access_token']
            expires = body.get('expires_in', 0)
            self._token_expiry = datetime.now() + timedelta(seconds=expires)
            return body['access_token']
        raise MythicAuthenticationError("no access token in response")
