from unittest.mock import Mock, patch

import pytest

from hostedpi.picloud import PiCloud
from hostedpi.pi import Pi
from hostedpi.models.responses import PiInfoBasic, PiInfo, SSHKeysResponse, ProvisioningServer
from hostedpi.models.pi import Pi3ServerSpec, Pi4ServerSpec


@pytest.fixture
def pi3_spec():
    return Pi3ServerSpec()


@pytest.fixture
def pi4_spec():
    return Pi4ServerSpec()


@pytest.fixture
def pi1_info_json():
    return {
        "ip": "2a00:1098:8:ffff::1",
        "ssh_port": 5001,
        "disk_size": "10.00",
        "initialized_keys": True,
        "location": "MER",
        "power": True,
        "model": 3,
        "is_booting": True,
        "boot_progress": "Waiting for initial DHCP",
    }


@pytest.fixture
def pi2_info_json():
    return {
        "ip": "2a00:1098:8:ffff::2",
        "ssh_port": 5002,
        "disk_size": "10.00",
        "initialized_keys": True,
        "location": "MER",
        "power": True,
        "model": 4,
        "is_booting": True,
        "boot_progress": "Waiting for initial DHCP",
    }


@pytest.fixture
def pi1_info_response(pi1_info_json):
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = pi1_info_json
    return mock


@pytest.fixture
def pi2_info_response(pi2_info_json):
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = pi2_info_json
    return mock


def test_new_with_name(pi3_spec, pi4_spec):
    pi3 = Pi.new_with_name("pi3", spec=pi3_spec, api_url=Mock(), session=Mock())
    assert pi3.name == "pi3"

    pi4 = Pi.new_with_name("pi4", spec=pi4_spec, api_url=Mock(), session=Mock())
    assert pi4.name == "pi4"
