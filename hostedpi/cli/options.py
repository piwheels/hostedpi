from pathlib import Path
from typing import Annotated, Union

from typer import Option


server_name = Annotated[Union[str, None], Option(help="Name of the new Raspberry Pi server")]
model = Annotated[int, Option(help="Raspberry Pi Model", min=3, max=4)]
disk_size = Annotated[int, Option(help="Disk size in GB", min=10)]
memory = Annotated[Union[int, None], Option(help="Memory in GB", min=1, max=8)]
cpu_speed = Annotated[Union[int, None], Option(help="CPU speed in MHz", min=1500)]
os_image = Annotated[Union[str, None], Option(help="Operating system image")]
wait = Annotated[bool, Option(help="Wait and poll for status to be available before returning")]
ssh_key_path = Annotated[
    Union[Path, None], Option(help="Path to the SSH key to install on the Raspberry Pi servers")
]
ssh_import_github = Annotated[
    Union[list[str], None],
    Option("--github", "--gh", help="GitHub usernames to source SSH keys from"),
]
ssh_import_launchpad = Annotated[
    Union[list[str], None],
    Option("--launchpad", "--lp", help="Launchpad usernames to source SSH keys from"),
]
ipv6 = Annotated[bool, Option(help="Use the IPv6 connection method")]
yes = Annotated[bool, Option("--yes", "-y", help="Proceed without confirmation")]
number = Annotated[Union[int, None], Option(help="Number of Raspberry Pi servers to create", min=1)]
full_table = Annotated[bool, Option(help="Show full table of Raspberry Pi server info")]
filter_pattern_pi = Annotated[
    Union[str, None], Option(help="Search pattern for filtering server names")
]
filter_pattern_images = Annotated[
    Union[str, None], Option(help="Search pattern for filtering image names")
]
