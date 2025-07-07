from typing import Union

from pydantic import BaseModel, Field, FilePath

from ..utils import collect_ssh_keys


class SSHKeySources(BaseModel):
    """
    Sources for SSH keys to be added to Pi servers

    :type ssh_keys: set[str] | None
    :param ssh_keys: Set of SSH key strings

    :type ssh_key_path: :class:`~pathlib.Path` | None
    :param ssh_key_path: Path to an SSH key file

    :type github_usernames: set[str] | None
    :param github_usernames: Set of GitHub usernames to collect SSH keys for

    :type launchpad_usernames: set[str] | None
    :param launchpad_usernames: Set of Launchpad usernames to collect SSH keys for

    :raises pydantic_core.ValidationError:
        If the SSH key sources are invalid
    """

    ssh_keys: Union[set[str], None] = Field(default=None, description="Set of SSH key strings")
    ssh_key_path: Union[FilePath, None] = Field(default=None, description="Path to an SSH key file")
    github_usernames: Union[set[str], None] = Field(
        default=None, description="Set of GitHub usernames to collect SSH keys for"
    )
    launchpad_usernames: Union[set[str], None] = Field(
        default=None, description="Set of Launchpad usernames to collect SSH keys for"
    )

    def collect(self) -> Union[set[str], None]:
        """
        Collect SSH keys from various sources, and return them as a set of strings which can be
        added to a Pi by setting :attr:`~hostedpi.pi.Pi.ssh_keys`.
        """
        keys = collect_ssh_keys(
            ssh_keys=self.ssh_keys,
            ssh_key_path=self.ssh_key_path,
            github_usernames=self.github_usernames,
            launchpad_usernames=self.launchpad_usernames,
        )
        return keys if keys else None
