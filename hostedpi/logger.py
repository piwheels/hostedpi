import structlog
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HOSTEDPI_", env_file=".env", extra="ignore")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "ERROR"

    @field_validator("log_level", mode="before")
    def validate_log_level(cls, v):
        if v:
            return v.upper()


settings = Settings()

structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(settings.log_level))
