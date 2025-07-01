from unittest.mock import Mock, patch

import pytest

from hostedpi.picloud import PiCloud
from hostedpi.models import Pi3ServerSpec, Pi4ServerSpec


MYTHIC_SERVERS = "https://api.mythic-beasts.com/beta/pi/servers"
MYTHIC_ASYNC_LOCATION = "https://api.mythic-beasts.com/queue/pi/1234"


@pytest.fixture(autouse=True)
def patch_log_request():
    with patch("hostedpi.picloud.log_request"):
        yield


@pytest.fixture
def mock_auth():
    mock_auth_instance = Mock()
    mock_auth_instance._settings.id = "test_id"
    mock_auth_instance.session.get = Mock()
    return mock_auth_instance


@pytest.fixture(autouse=True)
def patch_mythicauth(mock_auth):
    with patch("hostedpi.picloud.MythicAuth") as mock_cls:
        mock_cls.return_value = mock_auth
        yield


@pytest.fixture
def mock_session(mock_auth):
    return mock_auth.session


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


def test_picloud_init():
    cloud = PiCloud()
    assert repr(cloud) == "<PiCloud id=test_id>"


def test_get_pis_none(mock_session, pis_response_none):
    cloud = PiCloud()
    mock_session.get.return_value = pis_response_none
    pis = cloud.pis
    assert mock_session.get.called
    assert mock_session.get.call_args[0][0] == MYTHIC_SERVERS
    assert len(pis) == 0


def test_get_pis(mock_session, pis_response):
    cloud = PiCloud()
    mock_session.get.return_value = pis_response
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


def test_create_pi3_with_name(mock_session):
    cloud = PiCloud()

    create_pi3_response = Mock()
    create_pi3_response.status_code = 202
    create_pi3_response.headers = {"Location": MYTHIC_ASYNC_LOCATION}

    pi3_spec = Pi3ServerSpec()
    mock_session.post.return_value = create_pi3_response
    pi = cloud.create_pi(name="pi3", spec=pi3_spec)
    assert mock_session.post.called
    assert mock_session.post.call_args[0][0] == f"{MYTHIC_SERVERS}/pi3"
    assert pi.name == "pi3"
    assert pi.memory == 1024
    assert pi.cpu_speed == 1200


def test_create_pi3_with_no_name(mock_session):
    cloud = PiCloud()

    create_pi3_response = Mock()
    create_pi3_response.status_code = 202
    create_pi3_response.headers = {"Location": MYTHIC_ASYNC_LOCATION}

    pi3_spec = Pi3ServerSpec()
    mock_session.post.return_value = create_pi3_response
    pi = cloud.create_pi(spec=pi3_spec)
    assert mock_session.post.called
    assert mock_session.post.call_args[0][0] == MYTHIC_SERVERS
    assert pi._status_url == MYTHIC_ASYNC_LOCATION
    assert pi.name is None
    assert pi.memory == 1024
    assert pi.cpu_speed == 1200
