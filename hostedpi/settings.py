from functools import cache
from typing import Literal

from pydantic import AnyHttpUrl, SecretStr, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="hostedpi_", env_file=".env", extra="ignore")

    id: str
    secret: SecretStr
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "ERROR"
    auth_url: AnyHttpUrl = "https://auth.mythic-beasts.com/login"
    api_url: AnyHttpUrl = "https://api.mythic-beasts.com/beta/pi/"

    @field_validator("log_level", mode="before")
    @classmethod
    def validate_log_level(cls, v):
        if v:
            return v.upper()


@cache
def get_settings() -> Settings:
    return Settings()
