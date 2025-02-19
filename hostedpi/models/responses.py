from typing import Union
from ipaddress import IPv6Address, IPv6Network

from pydantic import BaseModel, RootModel, Field, ConfigDict, model_validator


class AuthResponse(BaseModel):
    access_token: str
    expires_in: int


class PiInfoBasic(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    model: int
    memory: int
    cpu_speed: int


class ServersResponse(BaseModel):
    servers: dict[str, PiInfoBasic]


class ErrorResponse(BaseModel):
    error: str = ""


class ProvisioningServer(BaseModel):
    provision_status: str = Field(alias="status")


class PiInfoResponse(PiInfoBasic, ProvisioningServer):
    model_full: Union[str, None] = None
    is_booting: bool
    boot_progress: Union[str, None] = None
    power: bool
    ssh_port: int
    disk_size: Union[int, None] = None
    nic_speed: int
    ipv6_address: IPv6Address = Field(alias="ip")
    ipv6_network: IPv6Network = Field(alias="ip_routed")
    initialised_keys: bool
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
