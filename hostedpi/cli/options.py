from typing import Union
from typing_extensions import Annotated
from pathlib import Path

from typer import Option


server_name = Annotated[Union[str, None], Option(help="Name of the new Raspberry Pi server")]
disk_size = Annotated[Union[int, None], Option(help="Disk size in GB", min=10)]
memory = Annotated[Union[int, None], Option(help="Memory in MB", min=1024)]
cpu_speed = Annotated[Union[int, None], Option(help="CPU speed in MHz", min=1500)]
os_image = Annotated[str, Option(help="Operating system image")]
wait_for_dns = Annotated[bool, Option(help="Wait for DNS to be available before returning")]
wait_async = Annotated[
    bool, Option(help="Wait and poll for status to be available before returning")
]
ssh_key_path = Annotated[Union[Path, None], Option(help="Path to the SSH key to install on the Pi")]
ipv6 = Annotated[bool, Option(help="Use the IPv6 connection method")]
