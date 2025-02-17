from typing import Union
from pathlib import Path

import requests
from requests.exceptions import HTTPError

from .exc import HostedPiException


def ssh_import_id(
    *,
    github: Union[str, None] = None,
    launchpad: Union[str, None] = None,
) -> set[str]:
    """
    Returns a set of SSH keys imported from GitHub or Launchpad
    """
    if github is None and launchpad is None:
        raise HostedPiException("GitHub or Launchpad username must be provided")

    keys = set()
    if github is not None:
        url = f"https://github.com/{github}.keys"
        sep = "\n"
        keys |= fetch_keys(url, sep)
    if launchpad is not None:
        url = f"https://launchpad.net/~{launchpad}/+sshkeys"
        sep = "\r\n\n"
        keys |= fetch_keys(url, sep)

    return keys


def fetch_keys(url: str, sep: str) -> set[str]:
    """
    Retrieve keys from *url* and return a set of keys
    """
    r = requests.get(url)

    try:
        r.raise_for_status()
    except HTTPError as e:
        raise HostedPiException(e) from e

    return set(r.text.strip().split(sep))


def read_ssh_key(ssh_key_path: Path) -> str:
    """
    Read the SSH key from the given path and return the file contents
    """
    return ssh_key_path.read_text()


def parse_ssh_keys(
    ssh_keys: set[str, None] = None,
    ssh_key_path: Union[Path, None] = None,
    ssh_import_github: Union[set[str], str, None] = None,
    ssh_import_launchpad: Union[set[str], str, None] = None,
) -> set[str]:
    """
    Parse SSH keys from any of various sources
    """
    if type(ssh_import_github) is str:
        ssh_import_github = {ssh_import_github}
    if type(ssh_import_launchpad) is str:
        ssh_import_launchpad = {ssh_import_launchpad}

    ssh_keys_set = set()
    if ssh_keys:
        ssh_keys_set |= ssh_keys
    if ssh_key_path:
        ssh_keys_set |= {read_ssh_key(ssh_key_path)}
    if ssh_import_github:
        for username in ssh_import_github:
            ssh_keys_set |= ssh_import_id(github=username)
    if ssh_import_launchpad:
        for username in ssh_import_launchpad:
            ssh_keys_set |= ssh_import_id(launchpad=username)
    return ssh_keys_set
