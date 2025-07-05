from typing import Union
from datetime import datetime, timedelta
from importlib.metadata import version

from pydantic import ValidationError
from requests import HTTPError, Session
from structlog import get_logger

from .exc import MythicAuthenticationError
from .models.mythic.responses import AuthResponse
from .settings import get_settings, Settings


hostedpi_version = version("hostedpi")
logger = get_logger()


class MythicAuth:
    def __init__(
        self,
        *,
        login_url: str = "https://auth.mythic-beasts.com/login",
        settings: Union[Settings, None] = None,
    ):
        self._url = login_url
        if settings is None:
            settings = get_settings()
        self._settings = settings
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
        if self._token is None or datetime.now() > self._token_expiry:
            auth_session = Session()
            data = {"grant_type": "client_credentials"}
            creds = (self._settings.id, self._settings.secret.get_secret_value())
            logger.debug("Authenticating", client_id=self._settings.id)
            response = auth_session.post(self._url, auth=creds, data=data)

            try:
                response.raise_for_status()
            except HTTPError as exc:
                logger.debug("Failed to authenticate", error=str(exc))
                raise MythicAuthenticationError("Failed to authenticate") from exc

            try:
                body = AuthResponse.model_validate(response.json())
            except ValidationError as exc:
                logger.debug("Failed to validate auth response", error=str(exc))
                raise MythicAuthenticationError("Failed to validate auth response") from exc

            self._token = body.access_token
            self._token_expiry = datetime.now() + timedelta(seconds=body.expires_in)
            logger.debug("Got token", expires_in=body.expires_in, expires_at=self._token_expiry)
        return self._token
