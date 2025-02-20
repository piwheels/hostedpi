from typing_extensions import Annotated
from pathlib import Path

from typer import Argument


server_name = Annotated[str, Argument(help="Name of the Raspberry Pi server")]
model = Annotated[int, Argument(help="Model of the Raspberry Pi server", min=3, max=4)]
ssh_key_path = Annotated[
    Path, Argument(help="Path to the SSH key to install on the Raspberry Pi server")
]
