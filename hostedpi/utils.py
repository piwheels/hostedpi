from pathlib import Path
from typing import Literal, Union

import requests
from requests.exceptions import HTTPError
from structlog import get_logger

from .logger import log_request
from .models.mythic.responses import ErrorResponse


logger = get_logger()


def ssh_import_id(
    *,
    github_username: Union[str, None] = None,
    launchpad_username: Union[str, None] = None,
) -> set[str]:
    """
    Returns a set of SSH keys imported from GitHub and/or Launchpad
    """
    keys = set()
    if github_username is not None:
        url = f"https://github.com/{github_username}.keys"
        sep = "\n"
        keys |= {
            _add_ssh_import_tag(key, "gh", github_username) for key in fetch_keys_from_url(url, sep)
        }
    if launchpad_username is not None:
        url = f"https://launchpad.net/~{launchpad_username}/+sshkeys"
        sep = "\r\n\n"
        keys |= {
            _add_ssh_import_tag(key, "lp", launchpad_username)
            for key in fetch_keys_from_url(url, sep)
        }

    return keys


def fetch_keys_from_url(url: str, sep: str) -> set[str]:
    """
    Retrieve keys from *url* and return a set of keys
    """
    response = requests.get(url)
    log_request(response)
    response.raise_for_status()
    return set(response.text.strip().split(sep))


def collect_ssh_keys(
    *,
    ssh_keys: Union[set[str], None] = None,
    ssh_key_path: Union[Path, None] = None,
    github_usernames: Union[set[str], None] = None,
    launchpad_usernames: Union[set[str], None] = None,
) -> set[str]:
    """
    Collect and combine SSH keys from any of various sources
    """
    ssh_keys_set = set()
    if ssh_keys:
        ssh_keys_set |= ssh_keys
    if ssh_key_path:
        ssh_keys_set |= {ssh_key_path.read_text().strip()}
    if github_usernames:
        for username in github_usernames:
            ssh_keys_set |= ssh_import_id(github_username=username)
    if launchpad_usernames:
        for username in launchpad_usernames:
            ssh_keys_set |= ssh_import_id(launchpad_username=username)
    return dedupe_ssh_keys(ssh_keys_set)


def dedupe_ssh_keys(ssh_keys: set[str]) -> set[str]:
    """
    Deduplicate SSH keys by removing any duplicates that are identical except for the comment at the
    end of the key
    """

    def keysort(key: str) -> int:
        return (-key.count(" "), key)

    # sort keys by the number of spaces so we don't throw away any additional comments
    sorted_keys = sorted(ssh_keys, key=keysort)

    actual_keys = set()  # without comments
    unique_keys = set()  # with comments (returned)

    for key in sorted_keys:
        # Split the key into the actual key and the comment
        parts = key.split()
        actual_key = " ".join(parts[:2])
        if actual_key not in actual_keys:
            # Only add unique keys to the return set
            unique_keys.add(key)
            actual_keys.add(actual_key)

    return unique_keys


def get_error_message(exc: HTTPError) -> str:
    """
    Try to retrieve an error message from the response
    """
    try:
        data = exc.response.json()
    except Exception:
        if exc.response.text:
            return f"Error {exc.response.status_code}: {exc.response.text}"
        return f"Error {exc.response.status_code}"

    return ErrorResponse.model_validate(data).error


def remove_ssh_keys_by_label(ssh_keys: set[str], label: str) -> set[str]:
    """
    Remove SSH keys that have a specific label (e.g. ``user@hostname``)
    """
    if label:
        return {key for key in ssh_keys if _extract_ssh_key_label(key) != label}
    return ssh_keys


def remove_imported_ssh_keys(
    ssh_keys: set[str], source: Literal["gh", "lp"], username: str
) -> set[str]:
    """
    Remove SSH keys that were imported from a specific source (GitHub or Launchpad)
    """
    return {key for key in ssh_keys if not _is_imported_ssh_key(key, source, username)}


def _extract_ssh_key_label(key: str) -> Union[str, None]:
    """
    Try to extract the label (e.g. ``user@hostname``) from an SSH key string, otherwise return None
    """
    parts = key.split(" ")
    if len(parts) > 2 and "@" in parts[2]:
        return parts[2]


def _is_imported_ssh_key(key: str, source: Literal["gh", "lp"], username: str) -> bool:
    """
    Check if the SSH key was imported from a specific source (GitHub or Launchpad) and username
    """
    import_comment = f"# ssh-import-id {source}:{username}"
    return key.endswith(import_comment)


def _add_ssh_import_tag(key: str, source: str, username: str) -> str:
    """
    Add a tag to the SSH key to indicate it was imported
    """
    return f"{key} # ssh-import-id {source}:{username}"
