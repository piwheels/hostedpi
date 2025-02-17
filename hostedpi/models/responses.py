from typing import Union
from ipaddress import IPv6Address, IPv6Network

from pydantic import BaseModel, RootModel, Field, model_validator


class AuthResponse(BaseModel):
    access_token: str
    expires_in: int


class Server(BaseModel):
    model: int
    memory: int
    cpu_speed: int


class ServersResponse(BaseModel):
    servers: dict[str, Server]


class ErrorResponse(BaseModel):
    error: str = ""


class ServerResponse(BaseModel):
    ipv6_address: IPv6Address = Field(alias="ip")
    ipv6_network: IPv6Network = Field(alias="ip_routed")
    boot_progress: Union[str, None] = None
    power: bool
    is_booting: bool
    initialised_keys: bool
    provision_status: str = Field(alias="status")
    model: int
    model_full: Union[str, None] = None
    disk_size: Union[int, None] = None
    ssh_port: int
    cpu_speed: int
    nic_speed: int
    memory: int
    location: str


class SSHKeysResponse(BaseModel):
    keys_raw: str = Field(alias="ssh_key", default="")
    keys: set[str] = set()

    @model_validator(mode="after")
    def make_keys_set(self):
        self.keys = {key.strip() for key in self.keys_raw.split("\n") if key.strip()}
        return self


class PiImagesResponse(RootModel):
    root: dict[str, str]
