from datetime import datetime, timedelta
from importlib.metadata import version
from typing import Union

from pydantic import ValidationError
from requests import HTTPError, Session
from structlog import get_logger

from .exc import MythicAuthenticationError
from .models.mythic.responses import AuthResponse
from .settings import Settings


hostedpi_version = version("hostedpi")
logger = get_logger()


class MythicAuth:
    """
    This class handles authentication with the Mythic Beasts Hosted Pi API.

    It manages the access token used to authenticate requests to the API, and automatically
    refreshes it when it expires.

    :type settings: :class:`~hostedpi.settings.Settings` or None
    :param settings:
        The settings used to configure the API. If not provided, defaults to a new
        instance of :class:`~hostedpi.settings.Settings`.

    :type auth_session: :class:`requests.Session` or None
    :param auth_session:
        The session used to make authentication requests. If not provided, defaults to a new
        :class:`requests.Session`.

    :type api_session: :class:`requests.Session` or None
    :param api_session:
        The session used to make API requests. If not provided, defaults to a new
        :class:`requests.Session`.

    .. warning::
        This is for advanced use only. Most users should not need to interact with the
        authentication system directly, as it is handled automatically by
        :class:`~hostedpi.picloud.PiCloud`.

    :raises pydantic_core.ValidationError:
        If the provided settings are invalid or missing required fields.
    """

    def __init__(
        self,
        *,
        settings: Union[Settings, None] = None,
        auth_session: Union[Session, None] = None,
        api_session: Union[Session, None] = None,
    ):
        if settings is None:
            settings = Settings()
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
        """
        The session used to make requests to the Hosted Pi API
        """
        self._api_session.headers["Authorization"] = f"Bearer {self.token}"
        return self._api_session

    @property
    def settings(self) -> Settings:
        """
        The settings used to configure the API
        """
        return self._settings

    @property
    def token(self) -> str:
        """
        The access token used to authenticate requests to the API. The token is automatically
        refreshed when it expires.
        """
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
