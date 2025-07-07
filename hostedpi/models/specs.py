from typing import Literal, Union

from pydantic import BaseModel, Field, field_validator, model_validator


class NewServerSpec(BaseModel):
    disk: int = Field(default=10, description="Disk size in GB")
    model: int
    memory: int = 0
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
    """
    Specification model for the Raspberry Pi 3

    :type disk: int
    :param disk: Disk size in GB. Must be a multiple of 10, defaults to 10.

    :type os_image: str | None
    :param os_image:
        Operating system image to use. Defaults to None, which uses Mythic's default image.

    :raises pydantic_core.ValidationError:
        If the server specification is invalid
    """

    model: Literal[3] = 3
    memory: Union[Literal[1024], None] = None
    memory_gb: Literal[3] = Field(
        default=1,
        exclude=True,
        description="Memory in GB. Pi 3 only supports 1GB.",
    )
    cpu_speed: Literal[1200] = Field(
        default=1200,
        description="CPU speed in MHz. Pi 3 only supports 1200MHz.",
    )


class Pi4ServerSpec(NewServerSpec):
    """
    Specification model for the Raspberry Pi 4

    :type disk: int
    :param disk: Disk size in GB. Must be a multiple of 10, defaults to 10.

    :type memory_gb: int
    :param memory_gb: Memory in GB. Can be 4 or 8, defaults to 4.

    :type cpu_speed: int
    :param cpu_speed: CPU speed in MHz. Can be 1500 or 2000, defaults to 1500.

    :type os_image: str | None
    :param os_image:
        Operating system image to use. Defaults to None, which uses Mythic's default image.

    :raises pydantic_core.ValidationError:
        If the server specification is invalid
    """

    model: Literal[4] = 4
    memory: Union[Literal[4096, 8192], None] = None
    memory_gb: Literal[4, 8] = Field(
        default=4,
        exclude=True,
        description="Memory in GB. Pi 4 supports 4GB or 8GB",
    )
    cpu_speed: Literal[1500, 2000] = Field(
        default=1500,
        description="CPU speed in MHz. Pi 4 supports 1500MHz or 2000MHz.",
    )

    @model_validator(mode="after")
    def validate_memory_cpu_combo(self):
        if self.memory_gb == 4 and self.cpu_speed == 2000:
            raise ValueError("4GB Pi 4 only supports 1500MHz CPU speed")
        return self
