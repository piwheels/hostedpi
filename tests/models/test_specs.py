import pytest
from pydantic import ValidationError

from hostedpi.models.specs import NewServerSpec, Pi3ServerSpec, Pi4ServerSpec


def test_new_server_spec():
    spec = NewServerSpec(disk=10, model=4, memory_gb=2, cpu_speed=1500, os_image="red-star-os")
    assert spec.disk == 10
    assert spec.model == 4
    assert spec.memory_gb == 2
    assert spec.cpu_speed == 1500
    assert spec.os_image == "red-star-os"
    assert spec.memory == 2048


def test_new_server_spec_invalid_disk():
    with pytest.raises(ValidationError):
        NewServerSpec(disk=5, model=4, memory_gb=2, cpu_speed=1500)
    with pytest.raises(ValidationError):
        NewServerSpec(disk=15, model=4, memory_gb=2, cpu_speed=1500)


def test_new_server_spec_invalid_memory_cpu_combo():
    with pytest.raises(ValidationError):
        Pi4ServerSpec(disk=10, model=4, memory_gb=4, cpu_speed=2000)


def test_new_server_spec_valid_pi_3():
    spec = Pi3ServerSpec()
    assert spec.model == 3
    assert spec.memory_gb == 1
    assert spec.cpu_speed == 1200
    assert spec.memory == 1024


def test_new_server_spec_invalid_pi_3():
    with pytest.raises(ValidationError):
        Pi3ServerSpec(memory_gb=2)
    with pytest.raises(ValidationError):
        Pi3ServerSpec(cpu_speed=1500)
    with pytest.raises(ValidationError):
        Pi3ServerSpec(model=4)


def test_new_server_spec_valid_pi_4():
    spec = Pi4ServerSpec()
    assert spec.model == 4
    assert spec.memory_gb == 4
    assert spec.cpu_speed == 1500
    assert spec.memory == 4096

    spec = Pi4ServerSpec(memory_gb=8)
    assert spec.model == 4
    assert spec.memory_gb == 8
    assert spec.cpu_speed == 1500
    assert spec.memory == 8192

    spec = Pi4ServerSpec(memory_gb=8, cpu_speed=2000)
    assert spec.model == 4
    assert spec.memory_gb == 8
    assert spec.cpu_speed == 2000
    assert spec.memory == 8192
