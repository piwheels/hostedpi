from typing import Literal
import json

import structlog
from structlog import get_logger
from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import field_validator
from requests import Response


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_prefix="HOSTEDPI_", env_file=".env", extra="ignore")
    log_level: Literal["DEBUG", "INFO", "WARNING", "ERROR"] = "ERROR"

    @field_validator("log_level", mode="before")
    def validate_log_level(cls, v):
        if v:
            return v.upper()


settings = Settings()

structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(settings.log_level))

logger = get_logger()


def log_request(response: Response):
    """
    Log the request and response
    """
    logger.debug(
        "Sent request",
        url=response.url,
        method=response.request.method,
        status_code=response.status_code,
        body=json.loads(response.request.body.decode("utf-8")) if response.request.body else "",
    )

    try:
        response_body = response.json()
    except Exception:
        response_body = response.text
    logger.debug("Received response", body=response_body)
