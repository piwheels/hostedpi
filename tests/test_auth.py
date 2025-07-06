from datetime import timedelta
from unittest.mock import Mock, patch

import pytest
from requests import HTTPError

from hostedpi.auth import MythicAuth
from hostedpi.exc import MythicAuthenticationError
from hostedpi.settings import Settings


@pytest.fixture
def auth_id_2() -> str:
    return "test_id_2"


@pytest.fixture
def auth_secret_2() -> str:
    return "test_secret"


@pytest.fixture
def auth_url_2() -> str:
    return "http://localhost:8000/login"


@pytest.fixture
def api_url_2() -> str:
    return "http://localhost:8000/pi/"


@pytest.fixture
def settings_2(auth_id_2, auth_secret_2, auth_url_2, api_url_2) -> Settings:
    return Settings(id=auth_id_2, secret=auth_secret_2, auth_url=auth_url_2, api_url=api_url_2)


@pytest.fixture
def auth_2(settings_2) -> MythicAuth:
    return MythicAuth(settings=settings_2, auth_session=Mock(), api_session=Mock())


@pytest.fixture
def auth_response_with_server_error() -> Mock:
    return Mock(
        status_code=500,
        raise_for_status=Mock(side_effect=HTTPError),
    )


@pytest.fixture
def auth_response_with_invalid_body() -> Mock:
    return Mock(
        status_code=200,
        json=Mock(return_value={"error": "Invalid response"}),
    )


@patch("hostedpi.auth.datetime")
def test_auth_with_default_settings(
    mock_datetime, mock_dt, auth, auth_response, auth_response_2, auth_url
):
    mock_datetime.now.return_value = mock_dt
    auth._auth_session.post.side_effect = [auth_response, auth_response_2]

    assert repr(auth) == "<MythicAuth id=test_id>"

    assert auth.token == "foobar"
    assert auth._token_expiry == mock_dt + timedelta(seconds=3600)
    assert auth.session.headers["Authorization"] == "Bearer foobar"

    mock_datetime.now.return_value = mock_dt + timedelta(seconds=3601)
    assert auth.token == "barfoo"
    assert auth.session.headers["Authorization"] == "Bearer barfoo"

    assert auth._auth_session.post.call_count == 2
    assert auth._auth_session.post.call_args_list[0][0][0] == auth_url
    assert auth._auth_session.post.call_args_list[1][0][0] == auth_url


@patch("hostedpi.auth.datetime")
def test_auth_with_different_settings(
    mock_datetime, mock_dt, auth_2, auth_response, auth_response_2, auth_url_2
):
    mock_datetime.now.return_value = mock_dt
    auth_2._auth_session.post.side_effect = [auth_response, auth_response_2]

    assert repr(auth_2) == "<MythicAuth id=test_id_2>"

    assert auth_2.token == "foobar"
    assert auth_2._token_expiry == mock_dt + timedelta(seconds=3600)
    assert auth_2.session.headers["Authorization"] == "Bearer foobar"

    mock_datetime.now.return_value = mock_dt + timedelta(seconds=3601)
    assert auth_2.token == "barfoo"
    assert auth_2.session.headers["Authorization"] == "Bearer barfoo"

    assert auth_2._auth_session.post.call_count == 2
    assert auth_2._auth_session.post.call_args_list[0][0][0] == auth_url_2
    assert auth_2._auth_session.post.call_args_list[1][0][0] == auth_url_2


def test_auth_with_server_error(auth, auth_response_with_server_error):
    auth._auth_session.post.return_value = auth_response_with_server_error

    with pytest.raises(MythicAuthenticationError):
        auth.token


def test_auth_with_invalid_response(auth, auth_response_with_invalid_body):
    auth._auth_session.post.return_value = auth_response_with_invalid_body

    with pytest.raises(MythicAuthenticationError):
        auth.token
