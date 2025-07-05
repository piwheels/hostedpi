from typing import Literal, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class NewServerSpec(BaseModel):
    disk: int = Field(default=10, description="Disk size in GB (must be a multiple of 10).")
    model: int
    memory: int
    memory_gb: Union[int, None] = Field(default=None, exclude=True)
    cpu_speed: int
    os_image: Union[str, None] = Field(default=None, description="Operating system image")
    # wait_for_dns: bool = False

    @field_validator("disk", mode="after")
    @classmethod
    def validate_disk(cls, v):
        if v < 10:
            raise ValueError("Disk size must be at least 10GB")
        if v % 10 != 0:
            raise ValueError("Disk size must be a multiple of 10GB")
        return v

    @model_validator(mode="after")
    def convert_memory_gb_to_mb(self):
        if self.memory_gb is not None:
            self.memory = self.memory_gb * 1024
        return self


class Pi3ServerSpec(NewServerSpec):
    model: int = 3
    memory: Union[int, None] = None
    memory_gb: int = Field(
        default=1,
        exclude=True,
        description="Memory in GB. Pi 3 only supports 1GB.",
    )
    cpu_speed: int = Field(
        default=1200,
        description="CPU speed in MHz. Pi 3 only supports 1200MHz.",
    )


class Pi4ServerSpec(NewServerSpec):
    model: int = 4
    memory: Union[int, None] = None
    memory_gb: Literal[4, 8] = Field(
        default=4,
        exclude=True,
        description="Memory in GB. Pi 4 supports 4GB or 8GB, defaults to 4GB.",
    )
    cpu_speed: Literal[1500, 2000] = Field(
        default=1500,
        description="CPU speed in MHz. Pi 4 supports 1500MHz or 2000MHz, defaults to 1500MHz.",
    )

    @model_validator(mode="after")
    def validate_memory_cpu_combo(self):
        if self.cpu_speed == 2000 and self.memory_gb == 8:
            raise ValueError("8GB Pi 4 only supports 1500MHz CPU speed")
        return self
