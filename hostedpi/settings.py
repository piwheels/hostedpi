from pydantic import AnyHttpUrl, Field, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """
    This model handles the configuration settings for the Mythic Beasts Hosted Pi API.

    :type id: str
    :param id:
        Your API ID. Required to authenticate with the API.

    :type secret: str
    :param secret:
        Your API secret key. Required to authenticate with the API.

    :type auth_url: str
    :param auth_url:
        The authentication URL for the API. This is used to log in and obtain an access token.
        Defaults to "https://auth.mythic-beasts.com/login".

    :type api_url: str
    :param api_url:
        The base URL for the API. This is used to make requests to the API endpoints.
        Defaults to "https://api.mythic-beasts.com/beta/pi/".

    :raises pydantic_core.ValidationError:
        If the provided settings are invalid or missing required fields.
    """

    model_config = SettingsConfigDict(env_prefix="hostedpi_", env_file=".env", extra="ignore")

    id: str = Field(description="Your API ID")
    secret: SecretStr = Field(description="Your API secret key")
    auth_url: AnyHttpUrl = Field(
        default="https://auth.mythic-beasts.com/login",
        description="The authentication URL",
    )
    api_url: AnyHttpUrl = Field(
        default="https://api.mythic-beasts.com/beta/pi/",
        description="The API URL",
    )

    @field_validator("api_url", mode="before")
    @classmethod
    def ensure_trailing_slash(cls, v):
        if not v.endswith("/"):
            v += "/"
        return v
