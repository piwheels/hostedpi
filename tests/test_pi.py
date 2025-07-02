from unittest.mock import Mock, patch

import pytest

from hostedpi.pi import Pi


def test_pi_init(pi_info, mock_session, api_url):
    pi = Pi(name="test-pi", info=pi_info, api_url=api_url, session=mock_session)
    assert pi.name == "test-pi"
    assert pi.model == 3
    assert pi.memory == 1024
    assert pi.cpu_speed == 1200
    assert repr(pi) == "<Pi name=test-pi>"


def test_pi_get_info(pi_info, mock_session, api_url):
    pi = Pi(name="test-pi", info=pi_info, api_url=api_url, session=mock_session)

    # info = pi.info
