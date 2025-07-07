from pathlib import Path
from typing import Annotated, Union

from typer import Argument


server_name = Annotated[str, Argument(help="Name of the Raspberry Pi server")]
server_names = Annotated[Union[list[str], None], Argument(help="Names of the Raspberry Pi servers")]
ssh_key_path = Annotated[
    Path, Argument(help="Path to the SSH key to install on the Raspberry Pi servers")
]
images_model = Annotated[
    int, Argument(help="Raspberry Pi model number to list images for", min=3, max=4)
]
ssh_key_label = Annotated[str, Argument(help="Label for the SSH key, e.g. 'ben@finn'")]
