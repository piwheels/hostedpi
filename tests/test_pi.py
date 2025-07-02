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


def test_pi_init(pi3_spec, pi4_spec):
    pi3_info = PiInfoBasic.model_validate(pi3_spec)
    pi3 = Pi("pi1", info=pi3_info, api_url=Mock(), session=Mock())

    pi4_info = PiInfoBasic.model_validate(pi4_spec)
    pi4 = Pi("pi2", info=pi4_info, api_url=Mock(), session=Mock())
