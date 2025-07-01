from unittest.mock import Mock, patch

import pytest


@pytest.fixture
def pi1_info():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
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
    return mock


@pytest.fixture
def pi2_info():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
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
    return mock
