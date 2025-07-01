from unittest.mock import Mock, patch

import pytest

from hostedpi.picloud import PiCloud


MYTHIC_GET_SERVERS = "https://api.mythic-beasts.com/beta/pi/servers"


@pytest.fixture(autouse=True)
def patch_log_request():
    with patch("hostedpi.picloud.log_request"):
        yield


@pytest.fixture
def mock_auth():
    mock_auth_instance = Mock()
    mock_auth_instance._settings.id = "test_id"
    return mock_auth_instance


@pytest.fixture(autouse=True)
def patch_mythicauth(mock_auth):
    with patch("hostedpi.picloud.MythicAuth") as mock_cls:
        mock_cls.return_value = mock_auth
        yield


@pytest.fixture
def pis_response_none():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"servers": {}}
    return mock


@pytest.fixture
def pis_response():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "servers": {
            "pi1": {"model": 3, "memory": 1024, "cpu_speed": 1200},
            "pi2": {"model": 4, "memory": 4096, "cpu_speed": 1500},
        }
    }
    return mock


def test_picloud_init(mock_parse_ssh_keys):
    mock_parse_ssh_keys.return_value = set()
    cloud = PiCloud()
    assert repr(cloud) == "<PiCloud id=test_id>"


def test_get_pis_none(pis_response_none):
    mock_auth.session.get.return_value = pis_response_none
    cloud = PiCloud()
    pis = cloud.pis
    assert mock_auth.session.get.called
    assert mock_auth.session.get.call_args[0][0] == MYTHIC_GET_SERVERS
    assert len(pis) == 0


def test_get_pis(mock_auth, pis_response):
    mock_auth.session.get.return_value = pis_response
    cloud = PiCloud()
    pis = cloud.pis

    assert len(pis) == 2
    pi1, pi2 = pis
    assert pi1.name == "pi1"
    assert pi1.model == 3
    assert pi1.memory == 1024
    assert pi1.cpu_speed == 1200
    assert pi2.name == "pi2"
    assert pi2.model == 4
    assert pi2.memory == 4096
    assert pi2.cpu_speed == 1500
