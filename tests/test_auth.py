from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from requests import HTTPError

from hostedpi.auth import MythicAuth
from hostedpi.settings import Settings
from hostedpi.exc import MythicAuthenticationError


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
    return Mock(
        status_code=200,
        json=Mock(return_value={"access_token": "foobar", "expires_in": 3600}),
    )


@pytest.fixture
def auth_response_2():
    return Mock(
        status_code=200,
        json=Mock(return_value={"access_token": "barfoo", "expires_in": 3600}),
    )


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


@patch("hostedpi.auth.Session.post")
@patch("hostedpi.auth.get_settings")
def test_auth_with_server_error(mock_get_settings, mock_post, mock_settings, auth_response):
    mock_get_settings.return_value = mock_settings
    mock_post.return_value = auth_response
    auth_response.raise_for_status.side_effect = HTTPError
    auth = MythicAuth()

    with pytest.raises(MythicAuthenticationError):
        auth.token


@patch("hostedpi.auth.Session.post")
@patch("hostedpi.auth.get_settings")
def test_auth_with_invalid_response(mock_get_settings, mock_post, mock_settings, auth_response):
    mock_get_settings.return_value = mock_settings
    mock_post.return_value = auth_response
    auth_response.json.return_value = {}
    auth = MythicAuth()

    with pytest.raises(MythicAuthenticationError):
        auth.token
