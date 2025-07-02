from unittest.mock import Mock, patch
from ipaddress import IPv6Address, IPv6Network

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
    assert mock_session.get.call_count == 1
    assert mock_session.get.call_args[0][0] == api_url + "servers/test-pi"
    assert info == pi_info_full
    assert pi.model_full == "3B"
    assert not pi.is_booting
    assert pi.boot_progress == "booted"
    assert pi.power
    assert pi.ipv4_ssh_port == 5100
    assert pi.disk_size == 10
    assert pi.ipv4_ssh_command == "ssh -p 5100 root@ssh.test-pi.hostedpi.com"
    assert pi.ipv6_ssh_command == "ssh root@[2a00:1098:8:64::1]"
    assert pi.ipv6_address == IPv6Address("2a00:1098:8:64::1")
    assert pi.ipv6_network == IPv6Network("2a00:1098:0008:6400::/56")
    assert pi.initialised_keys is False
    assert pi.location == "CLL"
    v4c = "Host test-pi\n    user root\n    port 5100\n    hostname ssh.test-pi.hostedpi.com"
    assert pi.ipv4_ssh_config == v4c
    v6c = "Host test-pi\n    user root\n    hostname 2a00:1098:8:64::1"
    assert pi.ipv6_ssh_config == v6c
    assert pi.status == "Powered on"
    assert pi.provision_status == "live"
    assert pi.url == "http://www.test-pi.hostedpi.com"
    assert pi.url_ssl == "https://www.test-pi.hostedpi.com"


def test_pi_get_info_with_api_url(pi_info_basic, mock_session, api_url_2, pi_info_response):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url_2, session=mock_session)
    mock_session.get.return_value = pi_info_response
    pi.info
    assert mock_session.get.call_count == 1
    assert mock_session.get.call_args[0][0] == api_url_2 + "servers/test-pi"
