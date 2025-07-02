from unittest.mock import Mock, patch

import pytest

from hostedpi.pi import Pi


def test_pi_init(pi_info_basic, mock_session, api_url):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    assert pi.name == "test-pi"
    assert pi.model == 3
    assert pi.memory == 1024
    assert pi.cpu_speed == 1200
    assert repr(pi) == "<Pi name=test-pi>"


def test_pi_get_info(pi_info_basic, mock_session, api_url, pi_info_response, pi_info_full):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = pi_info_response
    info = pi.info
    assert info == pi_info_full
    assert pi.model_full == "3B"
    assert not pi.is_booting
    assert pi.boot_progress is None
    assert pi.power
    assert pi.ssh_port == 5100
    assert pi.disk_size == 10
    assert pi.ipv4_ssh_command == ""
