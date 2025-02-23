from functools import cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr, field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HOSTEDPI_", env_file=".env", extra="ignore")

    id: str
    secret: SecretStr
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "ERROR"

    @field_validator("log_level", mode="before")
    def validate_log_level(cls, v):
        if v:
            return v.upper()


@cache
def get_settings() -> Settings:
    return Settings()
