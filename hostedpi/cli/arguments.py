from typing import Union, Annotated
from pathlib import Path

from typer import Argument


server_name = Annotated[str, Argument(help="Name of the Raspberry Pi server")]
server_names = Annotated[Union[list[str], None], Argument(help="Names of the Raspberry Pi servers")]
ssh_key_path = Annotated[
    Path, Argument(help="Path to the SSH key to install on the Raspberry Pi server")
]
images_model = Annotated[
    int, Argument(help="Model of Raspberry Pi server to list images for", min=3, max=4)
]
