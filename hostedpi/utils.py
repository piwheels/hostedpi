from typing import Union
from pathlib import Path

import requests
from requests.exceptions import HTTPError
from structlog import get_logger

from .exc import HostedPiException
from .logger import log_request
from .models.responses import ErrorResponse


logger = get_logger()


def ssh_import_id(
    *,
    github: Union[str, None] = None,
    launchpad: Union[str, None] = None,
) -> set[str]:
    """
    Returns a set of SSH keys imported from GitHub or Launchpad
    """
    keys = set()
    if github is not None:
        url = f"https://github.com/{github}.keys"
        sep = "\n"
        keys |= fetch_keys_from_url(url, sep)
    if launchpad is not None:
        url = f"https://launchpad.net/~{launchpad}/+sshkeys"
        sep = "\r\n\n"
        keys |= fetch_keys_from_url(url, sep)

    return keys


def fetch_keys_from_url(url: str, sep: str) -> set[str]:
    """
    Retrieve keys from *url* and return a set of keys
    """
    response = requests.get(url)
    log_request(response)

    try:
        response.raise_for_status()
    except HTTPError as exc:
        raise HostedPiException(str(exc)) from exc

    return set(response.text.strip().split(sep))


def collect_ssh_keys(
    *,
    ssh_keys: Union[set[str], None] = None,
    ssh_key_path: Union[Path, None] = None,
    ssh_import_github: Union[set[str], None] = None,
    ssh_import_launchpad: Union[set[str], None] = None,
) -> set[str]:
    """
    Collect and combine SSH keys from any of various sources
    """
    ssh_keys_set = set()
    if ssh_keys:
        ssh_keys_set |= ssh_keys
    if ssh_key_path:
        ssh_keys_set |= {ssh_key_path.read_text().strip()}
    if ssh_import_github:
        for username in ssh_import_github:
            ssh_keys_set |= ssh_import_id(github=username)
    if ssh_import_launchpad:
        for username in ssh_import_launchpad:
            ssh_keys_set |= ssh_import_id(launchpad=username)
    return ssh_keys_set


def get_error_message(exc: HTTPError) -> Union[str, None]:
    """
    Try to retrieve an error message from the response
    """
    try:
        data = exc.response.json()
    except Exception:
        if exc.response.text:
            return f"Error {exc.response.status_code}: {exc.response.text}"
        return f"Error {exc.response.status_code}"

    try:
        return ErrorResponse.model_validate(data).error
    except Exception:
        return
