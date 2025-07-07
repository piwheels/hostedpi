import json
import os

import structlog
from requests import Response
from structlog import get_logger


log_level = os.getenv("HOSTEDPI_LOG_LEVEL", "ERROR")
structlog.configure(wrapper_class=structlog.make_filtering_bound_logger(log_level))
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
        body=json.loads(_get_response_body(response)) if response.request.body else "",
    )

    try:
        response_body = response.json()
    except Exception:
        response_body = response.text
    logger.debug("Received response", body=response_body)


def _get_response_body(response: Response) -> str:
    if response.request.body:
        if isinstance(response.request.body, bytes):
            return response.request.body.decode("utf-8")
        return response.request.body
    return ""
