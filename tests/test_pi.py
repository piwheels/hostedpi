from ipaddress import IPv6Address, IPv6Network
from unittest.mock import Mock, patch

import pytest
from requests.exceptions import HTTPError, ConnectionError

from hostedpi.exc import HostedPiUserError
from hostedpi.models.sshkeys import SSHKeySources
from hostedpi.pi import Pi
from hostedpi.pi import (
    HostedPiNotAuthorizedError,
    HostedPiProvisioningError,
    HostedPiServerError,
    HostedPiUserError,
)


@pytest.fixture
def pi_info_provisioning_json():
    return {"status": "provisioning"}


@pytest.fixture
def pi_info_provisioning_response(pi_info_provisioning_json):
    return Mock(
        status_code=200,
        json=Mock(return_value=pi_info_provisioning_json),
    )


@pytest.fixture
def pi_info_installing_json(pi_info_json):
    pi_info_installing = pi_info_json.copy()
    pi_info_installing["status"] = "installing"
    return pi_info_installing


@pytest.fixture
def pi_info_installing_response(pi_info_installing_json):
    return Mock(
        status_code=200,
        json=Mock(return_value=pi_info_installing_json),
    )


@pytest.fixture
def pi_info_booting_response(pi_info_json):
    pi_info_booting = pi_info_json.copy()
    pi_info_booting["is_booting"] = True
    pi_info_booting["boot_progress"] = "waiting for initial DHCP"
    return Mock(
        status_code=200,
        json=Mock(return_value=pi_info_booting),
    )


@pytest.fixture
def pi_info_powered_off_response(pi_info_json):
    pi_info_powered_off = pi_info_json.copy()
    pi_info_powered_off["power"] = False
    return Mock(
        status_code=200,
        json=Mock(return_value=pi_info_powered_off),
    )


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


@pytest.fixture
def error_403():
    return Mock(
        status_code=403,
        raise_for_status=Mock(
            side_effect=HTTPError(response=Mock(json={"error": "Not authorised"}))
        ),
    )


@pytest.fixture
def error_409():
    return Mock(
        status_code=409,
        raise_for_status=Mock(
            side_effect=HTTPError(response=Mock(json={"error": "Server provisioning"}))
        ),
    )


@pytest.fixture
def error_500():
    return Mock(
        status_code=500,
        raise_for_status=Mock(side_effect=HTTPError(response=Mock(json={"error": "Server error"}))),
    )


@patch("hostedpi.pi.MythicAuth")
def test_pi_init_no_auth(pi_name, mythic_auth, pi_info_basic):
    pi = Pi(name=pi_name, info=pi_info_basic)
    assert pi.name == pi_name
    assert pi.model == 3
    assert pi.memory_mb == 1024
    assert pi.cpu_speed == 1200
    assert repr(pi) == "<Pi name=pi model=3>"


def test_pi_init(pi_name, pi_info_basic, auth):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    assert pi.name == "test-pi"
    assert pi.model == 3
    assert pi.memory_mb == 1024
    assert pi.cpu_speed == 1200
    assert repr(pi) == "<Pi name=test-pi model=3>"


def test_pi_init_with_full_info(pi_name, pi_info_basic, auth, pi_info_full):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value.json.return_value = pi_info_full
    assert pi.model_full == "3B"
    assert repr(pi) == "<Pi name=test-pi model=3B>"


def test_pi_get_info(pi_name, pi_info_basic, auth, pi_info_response, pi_info_full, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_response
    info = pi.info
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi"
    assert info == pi_info_full
    assert pi.model_full == "3B"
    assert not pi.is_booting
    assert pi.boot_progress == "booted"
    assert pi.power
    assert pi.ipv4_ssh_port == 5100
    assert pi.disk_size == 10
    assert pi.memory_mb == 1024
    assert pi.memory_gb == 1
    assert pi.nic_speed == 100
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


def test_pi_get_info_installing(pi_name, pi_info_basic, auth, pi_info_installing_response, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_installing_response
    pi_info = pi.info
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi"
    assert pi.provision_status == "installing"
    assert pi.status == "Provisioning: installing"


def test_pi_get_info_booting(pi_name, pi_info_basic, auth, pi_info_booting_response, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_booting_response
    pi_info = pi.info
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi"
    assert pi.provision_status == "live"
    assert pi.status == "Booting: waiting for initial DHCP"


def test_pi_get_info_powered_off(
    pi_name, pi_info_basic, auth, pi_info_powered_off_response, api_url
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_powered_off_response
    pi_info = pi.info
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi"
    assert pi.provision_status == "live"
    assert pi.status == "Powered off"


def test_pi_get_info_with_api_url(pi_name, pi_info_basic, auth_2, pi_info_response, api_url_2):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth_2)
    auth_2._api_session.get.return_value = pi_info_response
    pi.info
    assert auth_2._api_session.get.call_count == 1
    assert auth_2._api_session.get.call_args[0][0] == api_url_2 + "servers/test-pi"


def test_get_ssh_keys_403(pi_name, pi_info_basic, auth, error_403):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = error_403
    with pytest.raises(HostedPiNotAuthorizedError):
        keys = pi.ssh_keys


def test_get_ssh_keys_409(pi_name, pi_info_basic, auth, error_409):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = error_409
    with pytest.raises(HostedPiProvisioningError):
        keys = pi.ssh_keys


def test_get_ssh_keys_500(pi_name, pi_info_basic, auth, error_500):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = error_500
    with pytest.raises(HostedPiServerError):
        keys = pi.ssh_keys


def test_get_ssh_keys_empty(pi_name, pi_info_basic, auth, ssh_key_empty_response, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = ssh_key_empty_response
    keys = pi.ssh_keys
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    assert keys == set()


def test_get_ssh_keys(pi_name, pi_info_basic, auth, three_ssh_keys_response):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = three_ssh_keys_response
    keys = pi.ssh_keys
    assert keys == {"ssh-rsa AAA", "ssh-rsa BBB", "ssh-rsa CCC"}


def test_set_ssh_keys_403(pi_name, pi_info_basic, auth, error_403):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.put.return_value = error_403
    with pytest.raises(HostedPiNotAuthorizedError):
        pi.ssh_keys = None


def test_set_ssh_keys_409(pi_name, pi_info_basic, auth, error_409):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.put.return_value = error_409
    with pytest.raises(HostedPiProvisioningError):
        pi.ssh_keys = None


def test_set_ssh_keys_500(pi_name, pi_info_basic, auth, error_500):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.put.return_value = error_500
    with pytest.raises(HostedPiServerError):
        pi.ssh_keys = None


def test_unset_ssh_keys(pi_name, pi_info_basic, auth, one_ssh_key_response):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.put.return_value = one_ssh_key_response
    pi.ssh_keys = None
    assert auth._api_session.put.call_count == 1
    json_payload = auth._api_session.put.call_args[1]["json"]
    assert json_payload == {"ssh_key": ""}


def test_set_one_ssh_key(pi_name, pi_info_basic, auth, one_ssh_key_response, one_ssh_key):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.put.return_value = one_ssh_key_response
    pi.ssh_keys = one_ssh_key
    assert auth._api_session.put.call_count == 1
    json_payload = auth._api_session.put.call_args[1]["json"]
    assert json_payload == {"ssh_key": "ssh-rsa AAA"}


def test_add_one_ssh_key(
    pi_name, pi_info_basic, auth, ssh_key_empty_response, one_ssh_key_response, one_ssh_key
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = ssh_key_empty_response
    auth._api_session.put.return_value = one_ssh_key_response
    pi.ssh_keys |= one_ssh_key
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.put.call_count == 1
    json_payload = auth._api_session.put.call_args[1]["json"]
    assert json_payload == {"ssh_key": "ssh-rsa AAA"}


def test_add_ssh_keys(
    pi_name, pi_info_basic, auth, ssh_key_empty_response, one_ssh_key_response, three_ssh_keys
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = ssh_key_empty_response
    auth._api_session.put.return_value = one_ssh_key_response
    pi.ssh_keys |= three_ssh_keys
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.put.call_count == 1
    ssh_keys_data = auth._api_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAA" in ssh_keys_data
    assert "ssh-rsa BBB" in ssh_keys_data
    assert "ssh-rsa CCC" in ssh_keys_data
    assert ssh_keys_data.count("\r\n") == 2


def test_add_another_ssh_key(
    pi_name,
    pi_info_basic,
    auth,
    one_ssh_key_response,
    another_ssh_key,
    another_ssh_key_response,
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = one_ssh_key_response
    auth._api_session.put.return_value = another_ssh_key_response
    pi.ssh_keys |= another_ssh_key
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.put.call_count == 1
    ssh_keys_data = auth._api_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAA" in ssh_keys_data
    assert "ssh-rsa ZZZ" in ssh_keys_data
    assert ssh_keys_data.count("\r\n") == 1


def test_power_on_pi(pi_name, pi_info_basic, auth, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    pi.on()
    assert auth._api_session.put.call_count == 1
    assert auth._api_session.put.call_args[0][0] == api_url + "servers/test-pi/power"
    json_payload = auth._api_session.put.call_args[1]["json"]
    assert json_payload == {"power": True}


# def test_power_on_pi_with_wait(
#     pi_info_basic, auth, api_url, pi_info_booting_response, pi_info_response
# ):
#     auth._api_session.get.side_effect = [pi_info_booting_response, pi_info_response]
#     pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
#     pi.on(wait=True)
#     assert auth._api_session.put.call_count == 1
#     assert auth._api_session.put.call_args[0][0] == api_url + "servers/test-pi/power"
#     json_payload = auth._api_session.put.call_args[1]["json"]
#     assert json_payload == {"power": True}
#     assert auth._api_session.get.call_count == 2
#     assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi"
#     assert auth._api_session.get.call_args[1][0] == api_url + "servers/test-pi"


def test_power_off_pi(pi_name, pi_info_basic, auth, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    pi.off()
    assert auth._api_session.put.call_count == 1
    assert auth._api_session.put.call_args[0][0] == api_url + "servers/test-pi/power"
    json_payload = auth._api_session.put.call_args[1]["json"]
    assert json_payload == {"power": False}


def test_reboot_pi(pi_name, pi_info_basic, auth, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    pi.reboot()
    assert auth._api_session.post.call_count == 1
    assert auth._api_session.post.call_args[0][0] == api_url + "servers/test-pi/reboot"


def test_reboot_pi_403(pi_name, pi_info_basic, auth, error_403):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.post.return_value = error_403
    with pytest.raises(HostedPiNotAuthorizedError):
        pi.reboot()


def test_reboot_pi_409(pi_name, pi_info_basic, auth, error_409):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.post.return_value = error_409
    pi.reboot()  # should not raise an error, 409 means already rebooting


def test_reboot_pi_500(pi_name, pi_info_basic, auth, error_500):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.post.return_value = error_500
    with pytest.raises(HostedPiServerError):
        pi.reboot()


def test_cancel_pi(pi_name, pi_info_basic, auth, pi_info_response, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_response
    pi.cancel()
    assert auth._api_session.delete.call_count == 1
    assert auth._api_session.delete.call_args[0][0] == api_url + "servers/test-pi"
    assert pi._cancelled
    assert repr(pi) == "<Pi name=test-pi cancelled>"


def test_cancel_pi_again(pi_name, pi_info_basic, auth, pi_info_response, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_response
    pi.cancel()
    pi.cancel()  # should not raise an error, already cancelled
    # should not call the API again
    assert auth._api_session.delete.call_count == 1
    assert auth._api_session.delete.call_args[0][0] == api_url + "servers/test-pi"
    assert pi._cancelled
    assert repr(pi) == "<Pi name=test-pi cancelled>"


def test_cancel_pi_provisioning(
    pi_info_basic, auth, pi_info_provisioning_response, mythic_async_location
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth, status_url=mythic_async_location)
    auth._api_session.get.return_value = pi_info_provisioning_response
    pi.cancel()
    # should not call the API again
    assert auth._api_session.delete.call_count == 0
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == mythic_async_location
    assert not pi._cancelled
    assert repr(pi) == "<Pi name=test-pi model=3>"


def test_cancel_pi_error_403(pi_name, pi_info_basic, auth, api_url, pi_info_response, error_403):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_response
    auth._api_session.delete.return_value = error_403
    with pytest.raises(HostedPiNotAuthorizedError):
        pi.cancel()
    assert auth._api_session.delete.call_count == 1
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi"
    assert not pi._cancelled
    assert repr(pi) == "<Pi name=test-pi model=3B>"


def test_cancel_pi_error_409(pi_name, pi_info_basic, auth, api_url, pi_info_response, error_409):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_response
    auth._api_session.delete.return_value = error_409
    with pytest.raises(HostedPiProvisioningError):
        pi.cancel()
    assert auth._api_session.delete.call_count == 1
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi"
    assert not pi._cancelled
    assert repr(pi) == "<Pi name=test-pi model=3B>"


def test_cancel_pi_error_500(pi_name, pi_info_basic, auth, api_url, pi_info_response, error_500):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = pi_info_response
    auth._api_session.delete.return_value = error_500
    with pytest.raises(HostedPiServerError):
        pi.cancel()
    assert auth._api_session.delete.call_count == 1
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.get.call_args[0][0] == api_url + "servers/test-pi"
    assert not pi._cancelled
    assert repr(pi) == "<Pi name=test-pi model=3B>"


def test_add_ssh_keys(pi_name, pi_info_basic, auth, api_url):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value.json.return_value = {"ssh_key": ""}
    ssh_keys_set = {"ssh-rsa AAA", "ssh-rsa BBB", "ssh-rsa CCC"}
    ssh_keys = SSHKeySources(ssh_keys=ssh_keys_set)
    pi.add_ssh_keys(ssh_keys)
    assert auth._api_session.put.call_count == 1
    assert auth._api_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = auth._api_session.put.call_args[1]["json"]["ssh_key"]
    for key in ssh_keys_set:
        assert key in json_payload
    assert json_payload.count("\r\n") == len(ssh_keys_set) - 1


def test_remove_ssh_keys_no_label(
    pi_name, pi_info_basic, auth, imported_ssh_keys_response, api_url
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = imported_ssh_keys_response
    pi.remove_ssh_keys()
    assert auth._api_session.get.call_count == 1
    assert auth._api_session.put.call_count == 1
    assert auth._api_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = auth._api_session.put.call_args[1]["json"]["ssh_key"]
    assert json_payload == ""


def test_remove_ssh_keys_by_label(
    pi_name, pi_info_basic, auth, imported_ssh_keys_response, api_url
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = imported_ssh_keys_response
    pi.remove_ssh_keys("ben@finn")
    assert auth._api_session.get.call_count == 2
    assert auth._api_session.put.call_count == 1
    assert auth._api_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = auth._api_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAAA" not in json_payload
    assert "ssh-rsa BBBB" in json_payload
    assert "ssh-rsa CCCC" in json_payload
    assert "ssh-rsa DDDD" in json_payload
    assert "ssh-rsa EEEE" in json_payload
    assert "ssh-rsa FFFF" in json_payload


def test_unimport_ssh_keys_github(
    pi_name, pi_info_basic, auth, imported_ssh_keys_response, api_url
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = imported_ssh_keys_response
    pi.unimport_ssh_keys(github_usernames={"testuser"})
    assert auth._api_session.get.call_count == 2
    assert auth._api_session.put.call_count == 1
    assert auth._api_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = auth._api_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAAA" not in json_payload
    assert "ssh-rsa BBBB" not in json_payload
    assert "ssh-rsa CCCC" in json_payload
    assert "ssh-rsa DDDD" in json_payload
    assert "ssh-rsa EEEE" in json_payload
    assert "ssh-rsa FFFF" in json_payload
    assert "ssh-rsa GGGG" in json_payload


def test_unimport_ssh_keys_launchpad(
    pi_name, pi_info_basic, auth, imported_ssh_keys_response, api_url
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = imported_ssh_keys_response
    pi.unimport_ssh_keys(launchpad_usernames={"testuser4"})
    assert auth._api_session.get.call_count == 2
    assert auth._api_session.put.call_count == 1
    assert auth._api_session.put.call_args[0][0] == api_url + "servers/test-pi/ssh-key"
    json_payload = auth._api_session.put.call_args[1]["json"]["ssh_key"]
    assert "ssh-rsa AAAA" in json_payload
    assert "ssh-rsa BBBB" in json_payload
    assert "ssh-rsa CCCC" in json_payload
    assert "ssh-rsa DDDD" in json_payload
    assert "ssh-rsa EEEE" in json_payload
    assert "ssh-rsa FFFF" not in json_payload
    assert "ssh-rsa GGGG" not in json_payload


def test_get_provision_status_connnection_error(
    pi_name, pi_info_basic, auth, mythic_async_location
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth, status_url=mythic_async_location)
    auth._api_session.get.side_effect = ConnectionError("Connection error")
    status = pi.get_provision_status()
    assert status is None
    assert auth._api_session.get.call_count == 1


def test_get_provision_status_error_403(
    pi_name, pi_info_basic, auth, mythic_async_location, error_403
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth, status_url=mythic_async_location)
    auth._api_session.get.return_value = error_403
    with pytest.raises(HostedPiNotAuthorizedError):
        pi.get_provision_status()
    assert auth._api_session.get.call_count == 1


def test_get_provision_status_error_500(
    pi_name, pi_info_basic, auth, mythic_async_location, error_500
):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth, status_url=mythic_async_location)
    auth._api_session.get.return_value = error_500
    with pytest.raises(HostedPiServerError):
        pi.get_provision_status()
    assert auth._api_session.get.call_count == 1


def test_get_pi_info_without_a_name(pi_name, pi_info_basic, auth):
    pi = Pi(name=None, info=pi_info_basic, auth=auth)
    with pytest.raises(HostedPiUserError):
        pi.info


def test_get_pi_info_error_403(pi_name, pi_info_basic, auth, error_403):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = error_403
    with pytest.raises(HostedPiNotAuthorizedError):
        pi.info
    assert auth._api_session.get.call_count == 1


def test_get_pi_info_error_409(pi_name, pi_info_basic, auth, error_409):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = error_409
    with pytest.raises(HostedPiProvisioningError):
        pi.info
    assert auth._api_session.get.call_count == 1


def test_get_pi_info_error_500(pi_name, pi_info_basic, auth, error_500):
    pi = Pi(name=pi_name, info=pi_info_basic, auth=auth)
    auth._api_session.get.return_value = error_500
    with pytest.raises(HostedPiServerError):
        pi.info
    assert auth._api_session.get.call_count == 1
