from typing import Literal, Union
import string

from pydantic import BaseModel, field_validator


class SSHKeyBody(BaseModel):
    ssh_key: Union[str, None] = None

    @classmethod
    @field_validator("ssh_key", mode="after")
    def validate_ssh_key(cls, v):
        if v == "":
            return None
        return v


class NewServerSpec(SSHKeyBody):
    disk: int = 10
    ssh_key: Union[str, None] = None
    model: int
    memory: int
    cpu_speed: int
    os_image: Union[str, None] = None
    wait_for_dns: bool = False

    @classmethod
    @field_validator("disk", mode="after")
    def validate_disk(cls, v):
        if v < 10:
            raise ValueError("Disk size must be at least 10GB")
        if v % 10 != 0:
            raise ValueError("Disk size must be a multiple of 10GB")
        return v


class NewPi3ServerBody(NewServerSpec):
    model: int = 3
    memory: int = 1024
    cpu_speed: int = 1200


class NewPi4ServerBody(NewServerSpec):
    model: int = 4
    memory: Literal[4096, 8192] = 4096
    cpu_speed: Literal[1500, 2000] = 1500


class NewServer(BaseModel):
    name: str
    spec: Union[NewPi3ServerBody, NewPi4ServerBody]

    @classmethod
    @field_validator("name", mode="after")
    def validate_name(cls, v):
        server_name = v.lower()
        valid_chars = string.ascii_lowercase + string.digits + "-_"
        if not all(c in valid_chars for c in server_name):
            raise ValueError("Server name must consist of alphanumeric characters and hyphens")
        return v
