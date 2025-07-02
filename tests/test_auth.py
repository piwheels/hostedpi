from unittest.mock import Mock, patch
from datetime import timedelta

import pytest

from hostedpi.auth import MythicAuth
from hostedpi.settings import Settings


@pytest.fixture
def login_url():
    return "https://auth.mythic-beasts.com/login"


@pytest.fixture
def login_url_2():
    return "http://localhost:8000/"


@pytest.fixture
def mock_settings():
    return Settings(id="test_id", secret="test_secret")


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


@patch("hostedpi.auth.Session.post")
@patch("hostedpi.auth.get_settings")
@patch("hostedpi.auth.datetime")
def test_auth_with_default_login_url(
    mock_datetime,
    mock_get_settings,
    mock_post,
    mock_settings,
    mock_dt,
    auth_response,
    auth_response_2,
    login_url,
):
    mock_datetime.now.return_value = mock_dt
    mock_get_settings.return_value = mock_settings
    mock_post.side_effect = [auth_response, auth_response_2]

    auth = MythicAuth()
    assert repr(auth) == "<MythicAuth id=test_id>"

    assert auth.token == "foobar"
    assert auth._token_expiry == mock_dt + timedelta(seconds=3600)
    assert auth.session.headers["Authorization"] == "Bearer foobar"

    mock_datetime.now.return_value = mock_dt + timedelta(seconds=3601)
    assert auth.token == "barfoo"
    assert auth.session.headers["Authorization"] == "Bearer barfoo"

    assert mock_post.call_count == 2
    assert mock_post.call_args_list[0][0][0] == login_url
    assert mock_post.call_args_list[1][0][0] == login_url


@patch("hostedpi.auth.Session.post")
@patch("hostedpi.auth.get_settings")
def test_auth_with_login_url(
    mock_get_settings, mock_post, mock_settings, auth_response, login_url_2
):
    mock_get_settings.return_value = mock_settings
    mock_post.return_value = auth_response

    auth = MythicAuth(login_url=login_url_2)
    assert repr(auth) == "<MythicAuth id=test_id>"
    assert auth.token == "foobar"
    assert mock_post.call_args_list[0][0][0] == login_url_2
