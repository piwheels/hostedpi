from datetime import datetime, timedelta
from importlib.metadata import version
from typing import Union

from pydantic import ValidationError
from requests import HTTPError, Session
from structlog import get_logger

from .exc import MythicAuthenticationError
from .models.mythic.responses import AuthResponse
from .settings import Settings, get_settings


hostedpi_version = version("hostedpi")
logger = get_logger()


class MythicAuth:
    def __init__(
        self,
        *,
        settings: Union[Settings, None] = None,
        auth_session: Union[Session, None] = None,
        api_session: Union[Session, None] = None,
    ):
        if settings is None:
            settings = get_settings()
        if auth_session is None:
            auth_session = Session()
        if api_session is None:
            api_session = Session()
        self._settings = settings
        self._token = None
        self._token_expiry = datetime.now()
        api_session.headers = {
            "User-Agent": f"python-hostedpi/{hostedpi_version}",
        }
        self._auth_session = auth_session
        self._api_session = api_session

    def __repr__(self):
        return f"<MythicAuth id={self._settings.id}>"

    @property
    def session(self) -> Session:
        self._api_session.headers["Authorization"] = f"Bearer {self.token}"
        return self._api_session

    @property
    def settings(self) -> Settings:
        return self._settings

    @property
    def token(self) -> str:
        if self._token is None or datetime.now() > self._token_expiry:
            data = {"grant_type": "client_credentials"}
            creds = (self.settings.id, self.settings.secret.get_secret_value())
            logger.debug("Authenticating", client_id=self.settings.id)
            response = self._auth_session.post(str(self.settings.auth_url), auth=creds, data=data)

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
