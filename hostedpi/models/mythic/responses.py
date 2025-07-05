from ipaddress import IPv6Address, IPv6Network
from typing import Union

from pydantic import BaseModel, ConfigDict, Field, RootModel, model_validator


class AuthResponse(BaseModel):
    """
    Response from the Mythic Beasts Authentication API
    """

    access_token: str
    expires_in: int


class PiInfoBasic(BaseModel):
    """
    Basic information about a Raspberry Pi server, which comes back when listing servers
    """

    model_config = ConfigDict(from_attributes=True)

    model: int = Field(description="The model number of the Raspberry Pi server")
    memory: int = Field(description="The Pi's RAM size in MB")
    cpu_speed: int = Field(description="The Pi's CPU speed in MHz")

    @property
    def memory_gb(self) -> int:
        """
        The Pi's RAM size in GB
        """
        return self.memory // 1024


class ServersResponse(BaseModel):
    """
    Response from the Mythic Beasts API when listing servers
    """

    servers: dict[str, PiInfoBasic]


class ErrorResponse(BaseModel):
    """
    Response from the Mythic Beasts API when an API error occurs
    """

    error: str = "Error"


class ProvisioningServer(BaseModel):
    """
    Response from the Mythic Beasts API when a Raspberry Pi server is still provisioning
    """

    provision_status: str = Field(
        alias="status", description="The provisioning status of the server"
    )


class PiInfo(PiInfoBasic, ProvisioningServer):
    """
    Detailed information about a Raspberry Pi server, which comes back when retrieving details for a
    specific server
    """

    model_full: Union[str, None] = Field(
        default=None,
        description="The full model name of the server, e.g. 3B, 3B+ or 4B rather than just the model number",
    )
    is_booting: bool = Field(description="Whether the server is currently booting")
    boot_progress: Union[str, None] = Field(
        default=None, description="The server's current boot progress"
    )
    power: bool = Field(
        description="The server's power state, True if powered on, False if powered off"
    )
    ssh_port: int = Field(
        description="The SSH port that can be used to connect to the server using the IPv4 proxy"
    )
    disk_size: Union[int, None] = Field(default=None, description="The disk size in GB")
    nic_speed: int = Field(description="The network interface speed of the server in Mbps")
    ipv6_address: IPv6Address = Field(alias="ip", description="The IPv6 address of the server")
    ipv6_network: IPv6Network = Field(
        alias="ip_routed", description="The IPv6 network the server is on"
    )
    initialised_keys: bool = Field(description="Whether the server has initialised SSH keys")
    location: str = Field(description="The location of the data centre the server is in")


class SSHKeysResponse(BaseModel):
    """
    Response from the Mythic Beasts API when retrieving SSH keys
    """

    keys_raw: str = Field(alias="ssh_key", default="")
    keys: set[str] = set()

    @model_validator(mode="after")
    def make_keys_set(self):
        self.keys = {key.strip() for key in self.keys_raw.split("\n") if key.strip()}
        return self


class PiImagesResponse(RootModel):
    """
    Response from the Mythic Beasts API when retrieving available Pi images
    """

    root: dict[str, str]


class ServerSpec(BaseModel):
    """
    Details for a server specification, which comes back when retrieving available server
    specifications
    """

    disk: int = 10
    model: int
    memory: int
    cpu_speed: int
    nic_speed: int

    @property
    def memory_gb(self) -> int:
        return self.memory // 1024


class SpecsResponse(BaseModel):
    """
    Response from the Mythic Beasts API when retrieving available server specifications
    """

    models: list[ServerSpec]
