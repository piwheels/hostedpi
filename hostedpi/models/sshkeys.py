from typing import Union

from pydantic import BaseModel, FilePath

from ..utils import collect_ssh_keys


class SSHKeySources(BaseModel):
    ssh_keys: Union[set[str], None] = None
    ssh_key_path: Union[FilePath, None] = None
    github_usernames: Union[set[str], None] = None
    launchpad_usernames: Union[set[str], None] = None

    def collect(self) -> Union[set[str], None]:
        """
        Collect SSH keys from various sources
        """
        keys = collect_ssh_keys(
            ssh_keys=self.ssh_keys,
            ssh_key_path=self.ssh_key_path,
            github_usernames=self.github_usernames,
            launchpad_usernames=self.launchpad_usernames,
        )
        return keys if keys else None
