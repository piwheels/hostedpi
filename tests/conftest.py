from datetime import datetime
from typing import Union
from unittest.mock import Mock, patch

import pytest

from hostedpi.auth import MythicAuth
from hostedpi.models.mythic.responses import PiInfo, PiInfoBasic
from hostedpi.models.sshkeys import SSHKeySources
from hostedpi.settings import Settings


@pytest.fixture(autouse=True)
def unset_hostedpi_env(monkeypatch):
    monkeypatch.delenv("HOSTEDPI_ID", raising=False)
    monkeypatch.delenv("HOSTEDPI_SECRET", raising=False)
    monkeypatch.delenv("HOSTEDPI_LOG_LEVEL", raising=False)


@pytest.fixture
def mock_dt() -> datetime:
    return datetime(2025, 1, 1)


@pytest.fixture(autouse=True)
def patch_sleep():
    with patch("hostedpi.pi.sleep"):
        yield


@pytest.fixture(autouse=True)
def patch_log_request():
    with patch("hostedpi.picloud.log_request"):
        yield


@pytest.fixture(autouse=True)
def patch_log_request_pi():
    with patch("hostedpi.pi.log_request"):
        yield


@pytest.fixture
def auth_id() -> str:
    return "test_id"


@pytest.fixture
def auth_secret() -> str:
    return "test_secret"


@pytest.fixture
def auth_url() -> str:
    return "https://auth.mythic-beasts.com/login"


@pytest.fixture
def auth_url_2() -> str:
    return "http://localhost:8000/login"


@pytest.fixture
def api_url() -> str:
    return "https://api.mythic-beasts.com/beta/pi/"


@pytest.fixture
def api_url_2() -> str:
    return "http://localhost:8000/"


@pytest.fixture
def settings(auth_id, auth_secret, auth_url, api_url) -> Settings:
    return Settings(id=auth_id, secret=auth_secret, auth_url=auth_url, api_url=api_url)


@pytest.fixture
def auth_response() -> Mock:
    return Mock(
        status_code=200,
        json=Mock(return_value={"access_token": "foobar", "expires_in": 3600}),
    )


@pytest.fixture
def auth_response_2() -> Mock:
    return Mock(
        status_code=200,
        json=Mock(return_value={"access_token": "barfoo", "expires_in": 3600}),
    )


@pytest.fixture
def auth(settings, auth_response) -> MythicAuth:
    return MythicAuth(
        settings=settings,
        auth_session=Mock(post=Mock(return_value=auth_response)),
        api_session=Mock(),
    )


@pytest.fixture(autouse=True)
def collected_ssh_keys() -> set[str]:
    return {"ssh-rsa AAA", "ssh-rsa BBB", "ssh-rsa CCC"}


@pytest.fixture(autouse=True)
def ssh_keys(collected_ssh_keys) -> SSHKeySources:
    return SSHKeySources(ssh_keys=collected_ssh_keys)


@pytest.fixture
def settings_2(auth_id, auth_secret, auth_url_2, api_url_2) -> Settings:
    return Settings(id=auth_id, secret=auth_secret, auth_url=auth_url_2, api_url=api_url_2)


@pytest.fixture
def auth_2(settings_2, auth_response) -> MythicAuth:
    return MythicAuth(
        settings=settings_2,
        auth_session=Mock(post=Mock(return_value=auth_response)),
        api_session=Mock(),
    )


@pytest.fixture
def mythic_servers_url() -> str:
    return "https://api.mythic-beasts.com/beta/pi/servers"


@pytest.fixture
def mythic_async_location() -> str:
    return "https://api.mythic-beasts.com/queue/pi/1234"


@pytest.fixture
def pi_name() -> str:
    return "test-pi"


@pytest.fixture
def pi3_name() -> str:
    return "pi3"


@pytest.fixture
def pi4_name() -> str:
    return "pi4"


@pytest.fixture
def random_pi_name() -> str:
    return "abc123"


@pytest.fixture
def pi_info_json() -> dict[str, Union[str, int, bool, None]]:
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
def pi_info_2_json(pi_info_json) -> dict[str, Union[str, int, bool, None]]:
    pi_info_2_json = pi_info_json.copy()
    pi_info_2_json["ssh_port"] = "5123"
    pi_info_2_json["ip"] = "2a00:1098:0008:0064:0000:0000:0000:0002"
    return pi_info_2_json


@pytest.fixture
def pi_info_response(pi_info_json) -> Mock:
    return Mock(
        status_code=200,
        json=Mock(return_value=pi_info_json),
    )


@pytest.fixture
def pi_info_response_2(pi_info_2_json) -> Mock:
    return Mock(
        status_code=200,
        json=Mock(return_value=pi_info_2_json),
    )


@pytest.fixture
def pi_info_booting_response(pi_info_json) -> Mock:
    pi_info_booting_json = pi_info_json.copy()
    pi_info_booting_json["is_booting"] = True
    pi_info_booting_json["boot_progress"] = "booting"
    return Mock(
        status_code=200,
        json=Mock(return_value=pi_info_booting_json),
    )


@pytest.fixture
def pi_info_full(pi_info_json) -> PiInfo:
    return PiInfo.model_validate(pi_info_json)


@pytest.fixture
def pi_info_basic(pi_info_json) -> PiInfoBasic:
    return PiInfoBasic.model_validate(pi_info_json)


@pytest.fixture
def pi_info_response(pi_info_json, mythic_servers_url, pi3_name) -> Mock:
    return Mock(
        status_code=200,
        json=Mock(return_value=pi_info_json),
        request=Mock(url=f"{mythic_servers_url}/{pi3_name}"),
    )
