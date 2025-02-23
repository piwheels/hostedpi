import json

import structlog
from structlog import get_logger
from requests import Response

from .settings import get_settings


settings = get_settings()
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
