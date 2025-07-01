from typing import Union
import string

from pydantic import BaseModel, field_validator

from .pi import Pi3ServerSpec, Pi4ServerSpec


# class SSHKeyBody(BaseModel):
#     ssh_key: Union[str, None] = None

#     @field_validator("ssh_key", mode="before")
#     @classmethod
#     def validate_ssh_key(cls, v):
#         if v is None or v == "":
#             return "\n"
#         return v


class NewServer(BaseModel):
    name: Union[str, None] = None
    spec: Union[Pi3ServerSpec, Pi4ServerSpec]
    ssh_keys: Union[set[str], None] = None

    @field_validator("name", mode="after")
    @classmethod
    def validate_name(cls, v):
        if v is None or v == "":
            return None
        server_name = v.lower()
        valid_chars = string.ascii_lowercase + string.digits + "-"
        if not all(c in valid_chars for c in server_name):
            raise ValueError("Server name must consist of alphanumeric characters and hyphens")
        return server_name

    @field_validator("ssh_keys", mode="before")
    @classmethod
    def validate_ssh_keys(cls, v):
        if v == set():
            return None
        return v
