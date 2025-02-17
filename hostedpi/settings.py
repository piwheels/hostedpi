from functools import cache

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HOSTEDPI_", env_file=".env", extra="ignore")

    id: str
    secret: SecretStr


@cache
def get_settings() -> Settings:
    return Settings()
