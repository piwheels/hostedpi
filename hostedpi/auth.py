from datetime import datetime, timedelta
from importlib.metadata import version

from requests import Session, HTTPError
from pydantic import ValidationError

from .exc import MythicAuthenticationError
from .models.responses import AuthResponse
from .settings import get_settings


hostedpi_version = version("hostedpi")


class MythicAuth:
    def __init__(self):
        self._url = "https://auth.mythic-beasts.com/login"
        self._settings = get_settings()
        self._token = None
        self._token_expiry = datetime.now()
        self._session = Session()
        self._session.headers = {
            "User-Agent": f"python-hostedpi/{hostedpi_version}",
        }

    def __repr__(self):
        return f"<MythicAuth id={self._settings.id}>"

    @property
    def session(self) -> Session:
        self._session.headers["Authorization"] = f"Bearer {self.token}"
        return self._session

    @property
    def token(self) -> str:
        if datetime.now() > self._token_expiry:
            auth_session = Session()
            data = {"grant_type": "client_credentials"}
            creds = (self._settings.id, self._settings.secret.get_secret_value())
            response = auth_session.post(self._url, auth=creds, data=data)

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
