from unittest.mock import Mock

import pytest


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
