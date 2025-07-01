from typing import Union

from pydantic import BaseModel, FilePath

from ..utils import parse_ssh_keys


class SSHKeys(BaseModel):
    ssh_keys: Union[set[str], None] = None
    ssh_key_path: Union[FilePath, None] = None
    ssh_import_github: Union[set[str], None] = None
    ssh_import_launchpad: Union[set[str], None] = None

    def parse(self) -> Union[set[str], None]:
        keys = parse_ssh_keys(
            ssh_keys=self.ssh_keys,
            ssh_key_path=self.ssh_key_path,
            ssh_import_github=self.ssh_import_github,
            ssh_import_launchpad=self.ssh_import_launchpad,
        )
        return keys if keys else None
