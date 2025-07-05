from unittest.mock import Mock, patch

import pytest

from hostedpi.utils import (
    collect_ssh_keys,
    dedupe_ssh_keys,
    fetch_keys_from_url,
    get_error_message,
    remove_imported_ssh_keys,
    remove_ssh_keys_by_label,
    ssh_import_id,
)


@pytest.fixture(autouse=True)
def patch_log_request():
    with patch("hostedpi.utils.log_request"):
        yield


@pytest.fixture
def mock_github_response():
    return Mock(
        status_code=200,
        text="ssh-rsa foo\nssh-rsa bar",
    )


@pytest.fixture
def mock_launchpad_response():
    return Mock(
        status_code=200,
        text="ssh-rsa foobar\r\n\nssh-rsa barfoo",
    )


def test_dedupe_ssh_keys():
    keys = {
        "ssh-rsa foo",
        "ssh-rsa bar",
        "ssh-rsa foo",
    }
    deduped_keys = dedupe_ssh_keys(keys)
    assert deduped_keys == {"ssh-rsa foo", "ssh-rsa bar"}

    keys = {
        "ssh-rsa foo # ssh-import-id gh:testuser",
        "ssh-rsa bar",
        "ssh-rsa foo",
    }
    deduped_keys = dedupe_ssh_keys(keys)
    assert deduped_keys == {
        "ssh-rsa foo # ssh-import-id gh:testuser",
        "ssh-rsa bar",
    }

    keys = {
        "ssh-rsa foo testuser@home # ssh-import-id gh:testuser",
        "ssh-rsa bar testuser@home # ssh-import-id gh:testuser",
        "ssh-rsa foo testuser@home",
        "ssh-rsa bar testuser@home",
        "ssh-rsa foobar testuser@home",
        "ssh-rsa barfoo testuser@home",
        "ssh-rsa foo testuser@home # ssh-import-id lp:testuser2",
        "ssh-rsa bar testuser@home # ssh-import-id lp:testuser2",
        "ssh-rsa foobar testuser@home # ssh-import-id lp:testuser2",
        "ssh-rsa barfoo testuser@home # ssh-import-id lp:testuser2",
        "ssh-rsa foo",
        "ssh-rsa bar",
        "ssh-rsa foobar",
        "ssh-rsa barfoo",
    }
    deduped_keys = dedupe_ssh_keys(keys)
    assert deduped_keys == {
        "ssh-rsa bar testuser@home # ssh-import-id gh:testuser",
        "ssh-rsa barfoo testuser@home # ssh-import-id lp:testuser2",
        "ssh-rsa foo testuser@home # ssh-import-id gh:testuser",
        "ssh-rsa foobar testuser@home # ssh-import-id lp:testuser2",
    }


@patch("hostedpi.utils.requests.get")
def test_fetch_keys_github(mock_get, mock_github_response):
    mock_get.return_value = mock_github_response
    url = "https://example.com/keys"
    sep = "\n"
    keys = fetch_keys_from_url(url, sep)
    assert keys == {"ssh-rsa foo", "ssh-rsa bar"}


@patch("hostedpi.utils.requests.get")
def test_fetch_keys_launchpad(mock_get, mock_launchpad_response):
    mock_get.return_value = mock_launchpad_response
    url = "https://example.com/keys"
    sep = "\r\n\n"
    keys = fetch_keys_from_url(url, sep)
    assert keys == {"ssh-rsa foobar", "ssh-rsa barfoo"}


@patch("hostedpi.utils.requests.get")
def test_ssh_import_id_github(mock_get, mock_github_response):
    gh_user = "testuser"
    mock_get.return_value = mock_github_response
    keys = ssh_import_id(github_username=gh_user)
    assert mock_get.call_count == 1
    assert mock_get.call_args_list[0][0][0] == f"https://github.com/{gh_user}.keys"
    assert keys == {
        "ssh-rsa foo # ssh-import-id gh:testuser",
        "ssh-rsa bar # ssh-import-id gh:testuser",
    }


@patch("hostedpi.utils.requests.get")
def test_ssh_import_id_launchpad(mock_get, mock_launchpad_response):
    lp_user = "testuser2"
    mock_get.return_value = mock_launchpad_response
    keys = ssh_import_id(launchpad_username=lp_user)
    assert mock_get.call_count == 1
    assert mock_get.call_args_list[0][0][0] == f"https://launchpad.net/~{lp_user}/+sshkeys"
    assert keys == {
        "ssh-rsa foobar # ssh-import-id lp:testuser2",
        "ssh-rsa barfoo # ssh-import-id lp:testuser2",
    }


@patch("hostedpi.utils.requests.get")
def test_ssh_import_id_both(mock_get, mock_github_response, mock_launchpad_response):
    gh_user = "testuser"
    lp_user = "testuser2"
    mock_get.side_effect = [mock_github_response, mock_launchpad_response]
    keys = ssh_import_id(github_username=gh_user, launchpad_username=lp_user)
    assert mock_get.call_count == 2
    assert mock_get.call_args_list[0][0][0] == f"https://github.com/{gh_user}.keys"
    assert mock_get.call_args_list[1][0][0] == f"https://launchpad.net/~{lp_user}/+sshkeys"
    assert keys == {
        "ssh-rsa foo # ssh-import-id gh:testuser",
        "ssh-rsa bar # ssh-import-id gh:testuser",
        "ssh-rsa foobar # ssh-import-id lp:testuser2",
        "ssh-rsa barfoo # ssh-import-id lp:testuser2",
    }


def test_collect_ssh_keys_set():
    keys = collect_ssh_keys(ssh_keys={"ssh-rsa foo", "ssh-rsa bar"})
    assert keys == {"ssh-rsa foo", "ssh-rsa bar"}


def test_collect_ssh_keys_path(tmp_path):
    key_path = tmp_path / "id_rsa.pub"
    key_path.write_text("ssh-rsa foo")
    keys = collect_ssh_keys(ssh_key_path=key_path)
    assert keys == {"ssh-rsa foo"}


@patch("hostedpi.utils.requests.get")
def test_collect_ssh_keys_github(mock_get, mock_github_response):
    mock_get.return_value = mock_github_response
    keys = collect_ssh_keys(github_usernames={"testuser"})
    assert keys == {
        "ssh-rsa foo # ssh-import-id gh:testuser",
        "ssh-rsa bar # ssh-import-id gh:testuser",
    }


@patch("hostedpi.utils.requests.get")
def test_collect_ssh_keys_launchpad(mock_get, mock_launchpad_response):
    mock_get.return_value = mock_launchpad_response
    keys = collect_ssh_keys(launchpad_usernames={"testuser"})
    assert keys == {
        "ssh-rsa foobar # ssh-import-id lp:testuser",
        "ssh-rsa barfoo # ssh-import-id lp:testuser",
    }


@patch("hostedpi.utils.requests.get")
def test_collect_ssh_keys_all(mock_get, mock_github_response, mock_launchpad_response, tmp_path):
    mock_get.side_effect = [mock_github_response, mock_launchpad_response]
    key_path = tmp_path / "id_rsa.pub"
    key_path.write_text("ssh-rsa localkey")

    keys = collect_ssh_keys(
        ssh_keys={"ssh-rsa foo"},
        ssh_key_path=key_path,
        github_usernames={"testuser"},
        launchpad_usernames={"testuser2"},
    )

    assert keys == {
        "ssh-rsa foo # ssh-import-id gh:testuser",
        "ssh-rsa bar # ssh-import-id gh:testuser",
        "ssh-rsa foobar # ssh-import-id lp:testuser2",
        "ssh-rsa barfoo # ssh-import-id lp:testuser2",
        "ssh-rsa localkey",
    }


def test_get_error_message_json():
    mock_response = Mock(
        json=Mock(return_value={"error": "Something went wrong"}),
        status_code=400,
    )
    mock_exc = Mock(response=mock_response)
    message = get_error_message(mock_exc)
    assert message == "Something went wrong"


def test_get_error_message_text():
    mock_exc = Mock(
        response=Mock(
            json=Mock(side_effect=Exception),
            text="Something went wrong",
            status_code=400,
        )
    )
    message = get_error_message(mock_exc)
    assert message == "Error 400: Something went wrong"


def test_get_error_message_no_text():
    mock_exc = Mock(
        response=Mock(
            json=Mock(side_effect=Exception),
            text="",
            status_code=400,
        )
    )
    message = get_error_message(mock_exc)
    assert message == "Error 400"


def test_get_error_message_different_key():
    mock_response = Mock(
        json=Mock(return_value={"error but different key": "Something went really wrong"}),
        status_code=400,
    )
    mock_exc = Mock(response=mock_response)
    message = get_error_message(mock_exc)
    assert message == "Error"


def test_remove_ssh_keys_by_label():
    ssh_keys = {
        "ssh-rsa foo ben@finn # ssh-import-id gh:testuser",
        "ssh-rsa bar ben@jake",
        "ssh-rsa foobar dave@home # ssh-import-id lp:testuser2",
        "ssh-rsa barfoo # ssh-import-id lp:testuser2",
    }

    result = remove_ssh_keys_by_label(ssh_keys, "ben@finn")
    assert result == {
        "ssh-rsa bar ben@jake",
        "ssh-rsa foobar dave@home # ssh-import-id lp:testuser2",
        "ssh-rsa barfoo # ssh-import-id lp:testuser2",
    }

    result = remove_ssh_keys_by_label(ssh_keys, "dave@home")
    assert result == {
        "ssh-rsa foo ben@finn # ssh-import-id gh:testuser",
        "ssh-rsa bar ben@jake",
        "ssh-rsa barfoo # ssh-import-id lp:testuser2",
    }

    result = remove_ssh_keys_by_label(ssh_keys, "")
    assert result == ssh_keys


def test_remove_imported_ssh_keys_github():
    ssh_keys = set()
    result = remove_imported_ssh_keys(ssh_keys, "gh", "testuser")
    assert result == set()

    ssh_keys = {
        "ssh-rsa foo ben@finn # ssh-import-id gh:testuser",
        "ssh-rsa bar ben@jake",
        "ssh-rsa foo bob@test # ssh-import-id gh:testuser2",
        "ssh-rsa foobar dave@home # ssh-import-id lp:testuser",
        "ssh-rsa barfoo # ssh-import-id lp:testuser",
    }

    result = remove_imported_ssh_keys(ssh_keys, "gh", "testuser")
    assert result == {
        "ssh-rsa bar ben@jake",
        "ssh-rsa foo bob@test # ssh-import-id gh:testuser2",
        "ssh-rsa foobar dave@home # ssh-import-id lp:testuser",
        "ssh-rsa barfoo # ssh-import-id lp:testuser",
    }

    result = remove_imported_ssh_keys(ssh_keys, "gh", "testuser2")
    assert result == {
        "ssh-rsa foo ben@finn # ssh-import-id gh:testuser",
        "ssh-rsa bar ben@jake",
        "ssh-rsa foobar dave@home # ssh-import-id lp:testuser",
        "ssh-rsa barfoo # ssh-import-id lp:testuser",
    }
    result = remove_imported_ssh_keys(ssh_keys, "gh", "testuser3")
    assert result == ssh_keys


def test_remove_imported_ssh_keys_launchpad():
    ssh_keys = set()
    result = remove_imported_ssh_keys(ssh_keys, "lp", "testuser")
    assert result == set()

    ssh_keys = {
        "ssh-rsa foo ben@finn # ssh-import-id gh:testuser",
        "ssh-rsa bar ben@jake",
        "ssh-rsa foo bob@test # ssh-import-id lp:testuser2",
        "ssh-rsa foobar dave@home # ssh-import-id lp:testuser",
        "ssh-rsa barfoo # ssh-import-id lp:testuser",
    }

    result = remove_imported_ssh_keys(ssh_keys, "lp", "testuser")
    assert result == {
        "ssh-rsa foo ben@finn # ssh-import-id gh:testuser",
        "ssh-rsa bar ben@jake",
        "ssh-rsa foo bob@test # ssh-import-id lp:testuser2",
    }

    result = remove_imported_ssh_keys(ssh_keys, "lp", "testuser2")
    assert result == {
        "ssh-rsa foo ben@finn # ssh-import-id gh:testuser",
        "ssh-rsa bar ben@jake",
        "ssh-rsa foobar dave@home # ssh-import-id lp:testuser",
        "ssh-rsa barfoo # ssh-import-id lp:testuser",
    }
    result = remove_imported_ssh_keys(ssh_keys, "lp", "testuser3")
    assert result == ssh_keys
