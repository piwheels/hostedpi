from datetime import datetime, timedelta
from importlib.metadata import version

from requests import Session, HTTPError
from pydantic import ValidationError

from .exc import MythicAuthenticationError
from .models.responses import AuthResponse


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
            response = self._session.post(self._LOGIN_URL, auth=self._creds, data=data)

            try:
                response.raise_for_status()
            except HTTPError as exc:
                print(response.text)
                raise MythicAuthenticationError("Failed to authenticate") from exc

            try:
                body = AuthResponse.model_validate(response.json())
            except ValidationError as exc:
                raise MythicAuthenticationError("No access token in response")

            self._token = body.access_token
            self._token_expiry = datetime.now() + timedelta(seconds=body.expires_in)
        return self._token
