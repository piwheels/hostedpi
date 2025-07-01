from typing import Literal, Union

from pydantic import BaseModel, field_validator


class NewServerSpec(BaseModel):
    disk: int = 10
    model: int
    memory: int
    cpu_speed: int
    os_image: Union[str, None] = None
    # wait_for_dns: bool = False

    @field_validator("disk", mode="after")
    @classmethod
    def validate_disk(cls, v):
        if v < 10:
            raise ValueError("Disk size must be at least 10GB")
        if v % 10 != 0:
            raise ValueError("Disk size must be a multiple of 10GB")
        return v


class Pi3ServerSpec(NewServerSpec):
    model: int = 3
    memory: int = 1024
    cpu_speed: int = 1200


class Pi4ServerSpec(NewServerSpec):
    model: int = 4
    memory: Literal[4096, 8192] = 4096
    cpu_speed: Literal[1500, 2000] = 1500
