from unittest.mock import Mock, patch

import pytest


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
def auth_response():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"access_token": "foobar", "expires_in": 3600}
    return mock


@pytest.fixture
def auth_response_2():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"access_token": "barfoo", "expires_in": 3600}
    return mock
