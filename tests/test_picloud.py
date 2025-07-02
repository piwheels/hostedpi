from unittest.mock import Mock

import pytest
from requests import HTTPError, ConnectionError

from hostedpi.picloud import PiCloud
from hostedpi.models import Pi3ServerSpec, Pi4ServerSpec
from hostedpi.exc import HostedPiException


@pytest.fixture
def default_pi3_spec():
    return Pi3ServerSpec()


@pytest.fixture
def default_pi4_spec():
    return Pi4ServerSpec()


@pytest.fixture
def pis_response_none():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {"servers": {}}
    return mock


@pytest.fixture
def pis_response():
    mock = Mock()
    mock.status_code = 200
    mock.json.return_value = {
        "servers": {
            "pi1": {"model": 3, "memory": 1024, "cpu_speed": 1200},
            "pi2": {"model": 4, "memory": 4096, "cpu_speed": 1500},
        }
    }
    return mock


@pytest.fixture
def pi3_images_response():
    return {
        "rpi-buster-armhf": "Raspberry Pi OS Buster (32 bit)",
        "rpi-bullseye-armhf": "Raspberry Pi OS Bullseye (32 bit)",
        "rpi-bullseye-arm64": "Raspberry Pi OS Bullseye (64 bit)",
        "rpi-focal-armhf": "Ubuntu 20.04 (Focal Fossa) (32 bit)",
        "rpi-buster-arm64": "Raspberry Pi OS Buster (64 bit)",
        "rpi-bookworm-arm64": "Raspberry Pi OS Bookworm (12) (64 bit)",
        "rpi-jammy-arm64": "Ubuntu 22.04 (Jammy Jellyfish) (64 bit)",
        "rpi-bookworm-armhf": "Raspberry Pi OS Bookworm (12) (32 bit)",
        "rpi-bionic-arm64": "Ubuntu 18.04 (Bionic Beaver) (64 bit)",
        "rpi-bullseye-arm64-vnc.2022-03-25T17:23:56+00:00": "Raspberry Pi OS Bullseye Desktop (64 bit, 1920x1080)",
        "rpi-focal-arm64": "Ubuntu 20.04 (Focal Fossa) (64 bit)",
    }


@pytest.fixture
def pi4_images_response():
    return {
        "rpi-buster-armhf": "Raspberry Pi OS Buster (32 bit)",
        "rpi-bullseye-armhf": "Raspberry Pi OS Bullseye (32 bit)",
        "rpi-bullseye-arm64": "Raspberry Pi OS Bullseye (64 bit)",
        "rpi-focal-armhf": "Ubuntu 20.04 (Focal Fossa) (32 bit)",
        "rpi-buster-arm64": "Raspberry Pi OS Buster (64 bit)",
        "rpi-bookworm-armhf": "Raspberry Pi OS Bookworm (12) (32 bit)",
        "rpi-jammy-arm64": "Ubuntu 22.04 (Jammy Jellyfish) (64 bit)",
        "rpi-bookworm-arm64": "Raspberry Pi OS Bookworm (12) (64 bit)",
        "rpi-bionic-arm64": "Ubuntu 18.04 (Bionic Beaver) (64 bit)",
        "rpi-bullseye-arm64-vnc.2022-03-25T17:23:56+00:00": "Raspberry Pi OS Bullseye Desktop (64 bit, 1920x1080)",
        "rpi-focal-arm64": "Ubuntu 20.04 (Focal Fossa) (64 bit)",
    }


@pytest.fixture
def create_pi_response(mythic_async_location):
    response = Mock()
    response.status_code = 202
    response.headers = {"Location": mythic_async_location}
    return response


@pytest.fixture
def out_of_stock_response():
    response = Mock()
    response.status_code = 503
    response.json.return_value = {
        "error": "We do not have any servers of the specified type available"
    }
    response.raise_for_status.side_effect = HTTPError(response=response)
    return response


@pytest.fixture
def provision_status_provisioning():
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "status": "Provisioning",
    }
    return response


@pytest.fixture
def provision_status_installing():
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "status": "Installing operating system",
    }
    return response


@pytest.fixture
def provision_status_booting():
    response = Mock()
    response.status_code = 200
    response.json.return_value = {
        "status": "Booting Raspberry Pi",
    }
    return response


@pytest.fixture
def pi_info_response_random_name(pi_info_json, mythic_servers_url, random_pi_name):
    response = Mock()
    response.status_code = 200
    response.json.return_value = pi_info_json
    response.request.url = f"{mythic_servers_url}/{random_pi_name}"
    return response


def test_picloud_init(api_url):
    cloud = PiCloud()
    assert repr(cloud) == "<PiCloud id=test_id>"
    assert cloud.ssh_keys is None
    assert cloud._api_url == api_url


def test_picloud_init_with_api_url(api_url_2):
    cloud = PiCloud(api_url=api_url_2)
    assert repr(cloud) == "<PiCloud id=test_id>"
    assert cloud._api_url == api_url_2


def test_picloud_init_with_ssh_keys(ssh_keys, collected_ssh_keys):
    cloud = PiCloud(ssh_keys)
    assert repr(cloud) == "<PiCloud id=test_id>"
    assert cloud.ssh_keys == collected_ssh_keys


def test_picloud_init_with_bad_ssh_keys():
    with pytest.raises(TypeError):
        PiCloud(ssh_keys={})

    with pytest.raises(TypeError):
        PiCloud(ssh_keys="foo")


def test_get_pi3_operating_systems(mock_session, pi3_images_response):
    cloud = PiCloud()
    mock_session.get.return_value = Mock(
        status_code=200,
        json=Mock(return_value=pi3_images_response),
    )
    images = cloud.get_operating_systems(model=3)
    assert images == pi3_images_response


def test_get_pi4_operating_systems(mock_session, pi4_images_response):
    cloud = PiCloud()
    mock_session.get.return_value = Mock(
        status_code=200,
        json=Mock(return_value=pi4_images_response),
    )
    images = cloud.get_operating_systems(model=3)
    assert images == pi4_images_response


def test_get_pis_none(mock_session, pis_response_none, mythic_servers_url):
    cloud = PiCloud()
    mock_session.get.return_value = pis_response_none
    pis = cloud.pis
    assert mock_session.get.called
    assert mock_session.get.call_args[0][0] == mythic_servers_url
    assert len(pis) == 0


def test_get_pis(mock_session, pis_response):
    cloud = PiCloud()
    mock_session.get.return_value = pis_response
    pis = cloud.pis

    assert len(pis) == 2
    pi1, pi2 = pis
    assert pi1.name == "pi1"
    assert pi1.model == 3
    assert pi1.memory == 1024
    assert pi1.cpu_speed == 1200
    assert pi2.name == "pi2"
    assert pi2.model == 4
    assert pi2.memory == 4096
    assert pi2.cpu_speed == 1500


def test_new_pi_bad_name():
    cloud = PiCloud()
    for name in ["pi 3", "pi_3", "pi3@server", "pi3#server", "pi3.hostedpi.com"]:
        with pytest.raises(TypeError):
            cloud.create_pi(name=name, spec=default_pi3_spec)


def test_new_pi_good_name(mock_session, create_pi_response, default_pi3_spec):
    cloud = PiCloud()
    mock_session.post.return_value = create_pi_response
    for name in ["pi3", "pi-3", "3-pi", "pi3-hostedpi-com"]:
        pi = cloud.create_pi(name=name, spec=default_pi3_spec)
        assert pi.name == name


def test_create_pi3_with_name(
    mock_session, create_pi_response, mythic_servers_url, default_pi3_spec, pi3_name
):
    cloud = PiCloud()
    mock_session.post.return_value = create_pi_response
    pi = cloud.create_pi(name=pi3_name, spec=default_pi3_spec)

    assert mock_session.post.called
    called_url = mock_session.post.call_args[0][0]
    assert called_url == f"{mythic_servers_url}/{pi3_name}"
    assert pi.name == pi3_name
    assert pi.memory == 1024
    assert pi.cpu_speed == 1200


def test_create_pi3_with_no_name(
    mock_session, create_pi_response, default_pi3_spec, mythic_servers_url, mythic_async_location
):
    cloud = PiCloud()
    mock_session.post.return_value = create_pi_response
    pi = cloud.create_pi(spec=default_pi3_spec)

    assert mock_session.post.called
    called_url = mock_session.post.call_args[0][0]
    assert called_url == mythic_servers_url
    assert pi._status_url == mythic_async_location
    assert pi.name is None
    assert pi.memory == 1024
    assert pi.cpu_speed == 1200


def test_create_pi4_with_name(
    mock_session, create_pi_response, default_pi4_spec, mythic_servers_url
):
    cloud = PiCloud()
    mock_session.post.return_value = create_pi_response
    pi = cloud.create_pi(name="pi4", spec=default_pi4_spec)

    assert mock_session.post.called
    called_url = mock_session.post.call_args[0][0]
    assert called_url == f"{mythic_servers_url}/pi4"
    assert pi.name == "pi4"
    assert pi.memory == 4096
    assert pi.cpu_speed == 1500


def test_create_pi4_with_no_name(
    mock_session, create_pi_response, default_pi4_spec, mythic_servers_url, mythic_async_location
):
    cloud = PiCloud()
    mock_session.post.return_value = create_pi_response
    pi = cloud.create_pi(spec=default_pi4_spec)

    assert mock_session.post.called
    called_url = mock_session.post.call_args[0][0]
    assert called_url == mythic_servers_url
    assert pi._status_url == mythic_async_location
    assert pi.name is None
    assert pi.memory == 4096
    assert pi.cpu_speed == 1500


def test_create_pi_with_default_ssh_keys(
    mock_session,
    ssh_keys,
    create_pi_response,
    default_pi3_spec,
    mythic_servers_url,
    collected_ssh_keys,
):
    cloud = PiCloud(ssh_keys)
    mock_session.post.return_value = create_pi_response
    cloud.create_pi(name="pi3", spec=default_pi3_spec)
    assert mock_session.post.called
    called_url = mock_session.post.call_args[0][0]
    assert called_url == f"{mythic_servers_url}/pi3"
    assert "json" in mock_session.post.call_args[1]
    called_json = mock_session.post.call_args[1]["json"]
    assert "ssh_key" in called_json
    assert type(called_json["ssh_key"]) is str
    for key in collected_ssh_keys:
        assert key in called_json["ssh_key"]
    assert called_json["ssh_key"].count("\n") == len(collected_ssh_keys) - 1


def test_create_pi_with_ssh_keys(
    mock_session,
    ssh_keys,
    create_pi_response,
    default_pi3_spec,
    mythic_servers_url,
    collected_ssh_keys,
):
    cloud = PiCloud()
    mock_session.post.return_value = create_pi_response
    cloud.create_pi(name="pi3", spec=default_pi3_spec, ssh_keys=ssh_keys)
    assert mock_session.post.called
    called_url = mock_session.post.call_args[0][0]
    assert called_url == f"{mythic_servers_url}/pi3"
    assert "json" in mock_session.post.call_args[1]
    called_json = mock_session.post.call_args[1]["json"]
    assert "ssh_key" in called_json
    assert type(called_json["ssh_key"]) is str
    for key in collected_ssh_keys:
        assert key in called_json["ssh_key"]
    assert called_json["ssh_key"].count("\r\n") == len(collected_ssh_keys) - 1


def test_create_pi_named_with_wait(
    mock_session,
    create_pi_response,
    default_pi3_spec,
    provision_status_provisioning,
    provision_status_installing,
    provision_status_booting,
    pi_info_response,
    pi3_name,
):
    cloud = PiCloud()
    mock_session.post.return_value = create_pi_response
    mock_session.get.side_effect = [
        provision_status_provisioning,
        provision_status_installing,
        provision_status_installing,
        provision_status_booting,
        ConnectionError,
        pi_info_response,
    ]

    pi = cloud.create_pi(name=pi3_name, spec=default_pi3_spec, wait=True)
    assert mock_session.get.called
    assert mock_session.get.call_count == 6
    assert pi.name == pi3_name
    assert pi.model == 3
    assert pi.memory == 1024


def test_create_pi_unnamed_with_wait(
    mock_session,
    create_pi_response,
    default_pi3_spec,
    provision_status_provisioning,
    provision_status_installing,
    provision_status_booting,
    random_pi_name,
    pi_info_response_random_name,
):
    cloud = PiCloud()
    mock_session.post.return_value = create_pi_response
    mock_session.get.side_effect = [
        provision_status_provisioning,
        provision_status_installing,
        provision_status_installing,
        provision_status_booting,
        ConnectionError,
        pi_info_response_random_name,
    ]

    pi = cloud.create_pi(spec=default_pi3_spec, wait=True)
    assert mock_session.get.called
    assert mock_session.get.call_count == 6
    assert pi.name == random_pi_name
    assert pi.model == 3
    assert pi.memory == 1024


def test_create_pi_bad_spec(pi3_name):
    cloud = PiCloud()

    with pytest.raises(TypeError):
        cloud.create_pi(name=pi3_name, spec={})

    with pytest.raises(TypeError):
        cloud.create_pi(name=pi3_name, spec="foo")


def test_create_pi_bad_ssh_keys(pi3_name):
    cloud = PiCloud()

    with pytest.raises(TypeError):
        cloud.create_pi(name=pi3_name, spec=default_pi3_spec, ssh_keys={})

    with pytest.raises(TypeError):
        cloud.create_pi(name=pi3_name, spec=default_pi3_spec, ssh_keys="foo")


def test_create_pi_with_error(mock_session, out_of_stock_response, default_pi3_spec, pi3_name):
    cloud = PiCloud()
    mock_session.post.return_value = out_of_stock_response

    with pytest.raises(HostedPiException):
        cloud.create_pi(name=pi3_name, spec=default_pi3_spec)
