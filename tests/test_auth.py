from unittest.mock import patch
from datetime import datetime, timedelta

import pytest

from hostedpi.auth import MythicAuth
from hostedpi.settings import Settings


@pytest.fixture
def mock_dt():
    return datetime(2025, 1, 1)


@patch("hostedpi.auth.Session.post")
@patch("hostedpi.auth.get_settings")
@patch("hostedpi.auth.datetime")
def test_auth(mock_datetime, mock_get_settings, mock_post, mock_dt, auth_response, auth_response_2):
    mock_datetime.now.return_value = mock_dt
    mock_get_settings.return_value = Settings(id="test_id", secret="test_secret")
    mock_post.side_effect = [auth_response, auth_response_2]

    auth = MythicAuth()
    assert repr(auth) == "<MythicAuth id=test_id>"

    assert auth.token == "foobar"
    assert auth._token_expiry == mock_dt + timedelta(seconds=3600)
    assert auth.session.headers["Authorization"] == "Bearer foobar"

    mock_datetime.now.return_value = mock_dt + timedelta(seconds=3601)
    assert auth.token == "barfoo"
    assert auth.session.headers["Authorization"] == "Bearer barfoo"
