from typing import Union

from pydantic import BaseModel, Field, FilePath

from ..utils import collect_ssh_keys


class SSHKeySources(BaseModel):
    """
    Sources for SSH keys to be added to Pi servers

    :raises pydantic_core.ValidationError:
        If the SSH key sources are invalid
    """

    ssh_keys: Union[set[str], None] = Field(default=None, description="Set of SSH key strings")
    ssh_key_path: Union[FilePath, None] = Field(default=None, description="Path to an SSH key file")
    github_usernames: Union[set[str], None] = Field(
        default=None, description="Set of GitHub usernames to collect SSH keys from"
    )
    launchpad_usernames: Union[set[str], None] = Field(
        default=None, description="Set of Launchpad usernames to collect SSH keys from"
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
