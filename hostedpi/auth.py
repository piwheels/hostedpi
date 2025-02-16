from datetime import datetime, timedelta
from importlib.metadata import version

from requests import Session, HTTPError

from .exc import MythicAuthenticationError


hostedpi_version = version("hostedpi")


class MythicAuth:
    _LOGIN_URL = "https://auth.mythic-beasts.com/login"

    def __init__(self, api_id: str, api_secret: str):
        self._creds = (api_id, api_secret)
        self._token = None
        self._token_expiry = datetime.now()
        self._session = Session()
        self._session.headers = {
            "User-Agent": f"python-hostedpi/{hostedpi_version}",
        }

    def __repr__(self):
        return "<MythicAuth>"

    @property
    def session(self) -> Session:
        self._session.headers["Authorization"] = f"Bearer {self.token}"
        return self._session

    @property
    def token(self) -> str:
        if datetime.now() > self._token_expiry:
            data = {"grant_type": "client_credentials"}
            self._session.headers.pop("Authorization", None)
            self._session.headers.pop("Content-Type", None)
            r = self._session.post(self._LOGIN_URL, auth=self._creds, data=data)

            try:
                r.raise_for_status()
            except HTTPError as exc:
                print(r.text)
                raise MythicAuthenticationError("Failed to authenticate") from exc

            body = r.json()
            if "access_token" in body:
                self._token = body["access_token"]
                expires = body.get("expires_in", 0)
                self._token_expiry = datetime.now() + timedelta(seconds=expires)
                self._token = body["access_token"]
            else:
                raise MythicAuthenticationError("No access token in response")
        return self._token
