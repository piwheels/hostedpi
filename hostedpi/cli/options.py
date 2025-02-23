from typing import Union, Annotated
from pathlib import Path

from typer import Option


server_name = Annotated[Union[str, None], Option(help="Name of the new Raspberry Pi server")]
model = Annotated[int, Option(help="Raspberry Pi Model", min=3, max=4)]
disk_size = Annotated[Union[int, None], Option(help="Disk size in GB", min=10)]
memory = Annotated[Union[int, None], Option(help="Memory in MB", min=1024)]
cpu_speed = Annotated[Union[int, None], Option(help="CPU speed in MHz", min=1500)]
os_image = Annotated[str, Option(help="Operating system image")]
wait = Annotated[bool, Option(help="Wait and poll for status to be available before returning")]
ssh_key_path = Annotated[
    Union[Path, None], Option(help="Path to the SSH key to install on the Raspberry Pi server")
]
ssh_import_github = Annotated[
    Union[list[str], None], Option(help="Usernames to import SSH keys from GitHub")
]
ssh_import_launchpad = Annotated[
    Union[list[str], None], Option(help="Usernames to import SSH keys from Launchpad")
]
ipv6 = Annotated[bool, Option(help="Use the IPv6 connection method")]
yes = Annotated[bool, Option("--yes", "-y", help="Proceed without confirmation")]
number = Annotated[Union[int, None], Option(help="Number of Raspberry Pi servers to create", min=1)]
full_table = Annotated[bool, Option(help="Show full table of Raspberry Pi server info")]
filter_pattern = Annotated[Union[str, None], Option(help="Search pattern for filtering results")]
