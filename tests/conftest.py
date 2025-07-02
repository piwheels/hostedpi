from unittest.mock import Mock, patch

import pytest

from hostedpi.models.responses import PiInfoBasic


@pytest.fixture(autouse=True)
def unset_hostedpi_env(monkeypatch):
    monkeypatch.delenv("HOSTEDPI_ID", raising=False)
    monkeypatch.delenv("HOSTEDPI_SECRET", raising=False)
    monkeypatch.delenv("HOSTEDPI_LOG_LEVEL", raising=False)


@pytest.fixture(autouse=True)
def patch_sleep():
    with patch("hostedpi.pi.sleep"):
        yield


@pytest.fixture
def api_url():
    return "https://api.mythic-beasts.com/beta/pi/"


@pytest.fixture
def api_url_2():
    return "http://localhost:8000/"


@pytest.fixture
def mythic_servers_url():
    return "https://api.mythic-beasts.com/beta/pi/servers"


@pytest.fixture
def mythic_async_location():
    return "https://api.mythic-beasts.com/queue/pi/1234"


@pytest.fixture
def pi3_name():
    return "pi3"


@pytest.fixture
def pi4_name():
    return "pi4"


@pytest.fixture
def random_pi_name():
    return "abc123"


@pytest.fixture
def pi_info_json():
    return {
        "cpu_speed": 1200,
        "disk_size": "10.00",
        "model_full": "3B",
        "initialised_keys": False,
        "ip_routed": "2a00:1098:0008:6400:0000:0000:0000:0000/56",
        "ssh_port": 5100,
        "ip": "2a00:1098:0008:0064:0000:0000:0000:0001",
        "is_booting": False,
        "location": "CLL",
        "memory": 1024,
        "power": True,
        "nic_speed": 100,
        "status": "live",
        "model": 3,
        "boot_progress": None,
    }


@pytest.fixture
def pi_info(pi_info_json):
    return PiInfoBasic.model_validate(pi_info_json)


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
def pi_info_response(pi_info_json, mythic_servers_url, pi3_name):
    response = Mock()
    response.status_code = 200
    response.json.return_value = pi_info_json
    response.request.url = f"{mythic_servers_url}/{pi3_name}"
    return response
