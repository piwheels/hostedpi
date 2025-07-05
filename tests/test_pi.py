from ipaddress import IPv6Address, IPv6Network
from unittest.mock import Mock, patch

import pytest

from hostedpi.pi import Pi


@pytest.fixture
def ssh_key_empty_json():
    return {"ssh_key": ""}


@pytest.fixture
def ssh_key_empty_response(ssh_key_empty_json):
    return Mock(
        status_code=200,
        json=Mock(return_value=ssh_key_empty_json),
    )


@pytest.fixture
def ssh_three_keys_json():
    return {"ssh_key": "ssh-rsa AAA\r\n" "ssh-rsa BBB\r\n" "ssh-rsa CCC\r\n"}


@pytest.fixture
def three_ssh_keys_response(ssh_three_keys_json):
    return Mock(
        status_code=200,
        json=Mock(return_value=ssh_three_keys_json),
    )


@pytest.fixture
def one_ssh_key():
    return {"ssh-rsa AAA"}


@pytest.fixture
def three_ssh_keys():
    return {"ssh-rsa AAA", "ssh-rsa BBB", "ssh-rsa CCC"}


@pytest.fixture
def another_ssh_key():
    return {"ssh-rsa ZZZ"}


@pytest.fixture
def one_ssh_key_json():
    return {"ssh_key": "ssh-rsa AAA"}


@pytest.fixture
def another_ssh_key_json():
    return {"ssh_key": "ssh-rsa ZZZ"}


@pytest.fixture
def one_ssh_key_response(one_ssh_key_json):
    return Mock(
        status_code=200,
        json=Mock(return_value=one_ssh_key_json),
    )


@pytest.fixture
def another_ssh_key_response(another_ssh_key_json):
    return Mock(
        status_code=200,
        json=Mock(return_value=another_ssh_key_json),
    )


@pytest.fixture
def imported_ssh_keys_json():
    return {
        "ssh_key": (
            "ssh-rsa AAAA ben@finn # ssh-import-id gh:testuser\n"
            "ssh-rsa BBBB ben@jake # ssh-import-id gh:testuser\n"
            "ssh-rsa CCCC dave@home # ssh-import-id gh:testuser2\n"
            "ssh-rsa DDDD dave@work # ssh-import-id gh:testuser2\n"
            "ssh-rsa EEEE # ssh-import-id lp:testuser3\n"
            "ssh-rsa FFFF # ssh-import-id lp:testuser4\n"
            "ssh-rsa GGGG # ssh-import-id lp:testuser4\n"
        )
    }


@pytest.fixture
def imported_ssh_keys_response(imported_ssh_keys_json):
    return Mock(
        status_code=200,
        json=Mock(return_value=imported_ssh_keys_json),
    )


def test_pi_init(pi_info_basic, mock_session, api_url):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    assert pi.name == "test-pi"
    assert pi.model == 3
    assert pi.memory_mb == 1024
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


def test_get_ssh_keys_empty(pi_info_basic, mock_session, api_url, ssh_key_empty_response):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = ssh_key_empty_response
    keys = pi.ssh_keys
    assert mock_session.get.call_count == 1
    assert mock_session.get.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    assert keys == set()


def test_get_ssh_keys(pi_info_basic, mock_session, api_url, three_ssh_keys_response):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = three_ssh_keys_response
    keys = pi.ssh_keys
    assert keys == {"ssh-rsa AAA", "ssh-rsa BBB", "ssh-rsa CCC"}


def test_unset_ssh_keys(pi_info_basic, mock_session, api_url, one_ssh_key_response):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.put.return_value = one_ssh_key_response
    pi.ssh_keys = None
    assert mock_session.put.call_count == 1
    json_payload = mock_session.put.call_args[1]["json"]
    assert json_payload == {"ssh_key": ""}


def test_set_one_ssh_key(pi_info_basic, mock_session, api_url, one_ssh_key_response, one_ssh_key):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.put.return_value = one_ssh_key_response
    pi.ssh_keys = one_ssh_key
    assert mock_session.put.call_count == 1
    json_payload = mock_session.put.call_args[1]["json"]
    assert json_payload == {"ssh_key": "ssh-rsa AAA"}


def test_add_one_ssh_key(
    pi_info_basic, mock_session, api_url, ssh_key_empty_response, one_ssh_key_response, one_ssh_key
):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = ssh_key_empty_response
    mock_session.put.return_value = one_ssh_key_response
    pi.ssh_keys |= one_ssh_key
    assert mock_session.get.call_count == 1
    assert mock_session.put.call_count == 1
    json_payload = mock_session.put.call_args[1]["json"]
    assert json_payload == {"ssh_key": "ssh-rsa AAA"}


def test_add_ssh_keys(
    pi_info_basic,
    mock_session,
    api_url,
    ssh_key_empty_response,
    one_ssh_key_response,
    three_ssh_keys,
):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = ssh_key_empty_response
    mock_session.put.return_value = one_ssh_key_response
    pi.ssh_keys |= three_ssh_keys
    assert mock_session.get.call_count == 1
    assert mock_session.put.call_count == 1
    ssh_keys_data = mock_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAA" in ssh_keys_data
    assert "ssh-rsa BBB" in ssh_keys_data
    assert "ssh-rsa CCC" in ssh_keys_data
    assert ssh_keys_data.count("\r\n") == 2


def test_add_another_ssh_key(
    pi_info_basic,
    mock_session,
    api_url,
    one_ssh_key_response,
    another_ssh_key,
    another_ssh_key_response,
):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = one_ssh_key_response
    mock_session.put.return_value = another_ssh_key_response
    pi.ssh_keys |= another_ssh_key
    assert mock_session.get.call_count == 1
    assert mock_session.put.call_count == 1
    ssh_keys_data = mock_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAA" in ssh_keys_data
    assert "ssh-rsa ZZZ" in ssh_keys_data
    assert ssh_keys_data.count("\r\n") == 1


def test_power_on_pi(pi_info_basic, mock_session, api_url):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    pi.on()
    assert mock_session.put.call_count == 1
    assert mock_session.put.call_args[0][0] == api_url + "servers/test-pi/power"
    json_payload = mock_session.put.call_args[1]["json"]
    assert json_payload == {"power": True}


def test_power_off_pi(pi_info_basic, mock_session, api_url):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    pi.off()
    assert mock_session.put.call_count == 1
    assert mock_session.put.call_args[0][0] == api_url + "servers/test-pi/power"
    json_payload = mock_session.put.call_args[1]["json"]
    assert json_payload == {"power": False}


def test_reboot_pi(pi_info_basic, mock_session, api_url):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    pi.reboot()
    assert mock_session.post.call_count == 1
    assert mock_session.post.call_args[0][0] == api_url + "servers/test-pi/reboot"


def test_cancel_pi(pi_info_basic, mock_session, api_url, pi_info_response):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = pi_info_response
    pi.cancel()
    assert mock_session.delete.call_count == 1
    assert mock_session.delete.call_args[0][0] == api_url + "servers/test-pi"
    assert pi._cancelled
    assert repr(pi) == "<Pi name=test-pi cancelled>"


@patch("hostedpi.pi.collect_ssh_keys")
def test_ssh_import_id(collect_ssh_keys, pi_info_basic, mock_session, api_url):
    ssh_keys = {"ssh-rsa AAA", "ssh-rsa BBB", "ssh-rsa CCC"}
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    collect_ssh_keys.return_value = ssh_keys
    mock_session.get.return_value.json.return_value = {"ssh_key": ""}
    pi.import_ssh_keys(github_usernames={"testuser"}, launchpad_usernames={"testuser"})
    assert mock_session.put.call_count == 1
    assert mock_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = mock_session.put.call_args[1]["json"]["ssh_key"]
    for key in ssh_keys:
        assert key in json_payload
    assert json_payload.count("\r\n") == len(ssh_keys) - 1


def test_remove_ssh_keys_by_label(pi_info_basic, mock_session, api_url, imported_ssh_keys_response):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = imported_ssh_keys_response
    pi.remove_ssh_keys_by_label("ben@finn")
    assert mock_session.get.call_count == 2
    assert mock_session.put.call_count == 1
    assert mock_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = mock_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAAA" not in json_payload
    assert "ssh-rsa BBBB" in json_payload
    assert "ssh-rsa CCCC" in json_payload
    assert "ssh-rsa DDDD" in json_payload
    assert "ssh-rsa EEEE" in json_payload
    assert "ssh-rsa FFFF" in json_payload


def test_unimport_ssh_keys_github(pi_info_basic, mock_session, api_url, imported_ssh_keys_response):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = imported_ssh_keys_response
    pi.unimport_ssh_keys(github_usernames={"testuser"})
    assert mock_session.get.call_count == 2
    assert mock_session.put.call_count == 1
    assert mock_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = mock_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAAA" not in json_payload
    assert "ssh-rsa BBBB" not in json_payload
    assert "ssh-rsa CCCC" in json_payload
    assert "ssh-rsa DDDD" in json_payload
    assert "ssh-rsa EEEE" in json_payload
    assert "ssh-rsa FFFF" in json_payload
    assert "ssh-rsa GGGG" in json_payload


def test_unimport_ssh_keys_launchpad(
    pi_info_basic, mock_session, api_url, imported_ssh_keys_response
):
    pi = Pi(name="test-pi", info=pi_info_basic, api_url=api_url, session=mock_session)
    mock_session.get.return_value = imported_ssh_keys_response
    pi.unimport_ssh_keys(launchpad_usernames={"testuser4"})
    assert mock_session.get.call_count == 2
    assert mock_session.put.call_count == 1
    assert mock_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = mock_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAAA" in json_payload
    assert "ssh-rsa BBBB" in json_payload
    assert "ssh-rsa CCCC" in json_payload
    assert "ssh-rsa DDDD" in json_payload
    assert "ssh-rsa EEEE" in json_payload
    assert "ssh-rsa FFFF" not in json_payload
    assert "ssh-rsa GGGG" not in json_payload
