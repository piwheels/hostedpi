from unittest.mock import Mock, patch
from pathlib import Path

from typer.testing import CliRunner
import pytest
from requests import HTTPError

from hostedpi.cli import app
from hostedpi.pi import Pi


runner = CliRunner()


@pytest.fixture(autouse=True)
def mock_get_picloud():
    with patch("hostedpi.cli.utils.get_picloud") as get_picloud:
        yield get_picloud


@pytest.fixture()
def mock_pi(pi_name) -> Pi:
    pi = Mock()
    pi.name = pi_name
    pi.memory_gb = 1
    pi.cpu_speed = 1200
    pi.status = "Powered on"
    pi.ssh_keys = set()
    return pi


@pytest.fixture(autouse=True)
def mock_get_pis_one(mock_pi):
    with patch("hostedpi.cli.utils.get_pis") as get_pis:
        get_pis.return_value = [mock_pi]
        yield get_pis


@pytest.fixture()
def usage_text() -> str:
    return "Usage: hostedpi"


@pytest.fixture()
def help_text() -> str:
    return "Usage: hostedpi"


@pytest.fixture()
def ssh_key_path(tmp_path) -> str:
    key_path = tmp_path / "id_rsa.pub"
    key_path.write_text("ssh-rsa foo")
    return str(key_path)


def test_implicit_help(usage_text, help_text):
    result = runner.invoke(app, [])
    assert result.exit_code == 0
    assert usage_text in result.output
    assert help_text in result.output


def test_explicit_help(usage_text, help_text):
    result = runner.invoke(app, ["--help"])
    assert result.exit_code == 0
    assert usage_text in result.output
    assert help_text in result.output


def test_test_with_auth():
    result = runner.invoke(app, ["test"])
    assert result.exit_code == 0
    assert "Connected to the Mythic Beasts API" in result.output


def test_test_no_auth(mock_get_picloud):
    mock_get_picloud.side_effect = HTTPError
    result = runner.invoke(app, ["test"])
    assert result.exit_code > 0
    assert "Failed to authenticate" in result.output


def test_images():
    result = runner.invoke(app, ["images", "3"])
    assert result.exit_code == 0


def test_images_no_model():
    result = runner.invoke(app, ["images"])
    assert result.exit_code > 0
    assert "Missing argument 'MODEL'" in result.output


def test_list():
    result = runner.invoke(app, ["list"])
    assert result.exit_code == 0


def test_table():
    result = runner.invoke(app, ["table"])
    assert result.exit_code == 0


def test_create():
    result = runner.invoke(app, ["create", "--model", "3"])
    assert result.exit_code == 0


def test_status(pi_name):
    result = runner.invoke(app, ["status", pi_name])
    assert result.exit_code == 0


def test_on(pi_name):
    result = runner.invoke(app, ["on", pi_name])
    assert result.exit_code == 0


def test_off(pi_name):
    result = runner.invoke(app, ["off", pi_name])
    assert result.exit_code == 0


def test_reboot(pi_name):
    result = runner.invoke(app, ["reboot", pi_name])
    assert result.exit_code == 0


def test_cancel(pi_name):
    result = runner.invoke(app, ["cancel", pi_name, "--yes"])
    assert result.exit_code == 0


def test_ssh():
    result = runner.invoke(app, ["ssh"])
    assert result.exit_code == 0


def test_ssh_command(pi_name):
    result = runner.invoke(app, ["ssh", "command", pi_name])
    assert result.exit_code == 0


def test_ssh_config(pi_name):
    result = runner.invoke(app, ["ssh", "config", pi_name])
    assert result.exit_code == 0


def test_ssh_keys():
    result = runner.invoke(app, ["ssh", "keys"])
    assert result.exit_code == 0


def test_ssh_keys(pi_name):
    result = runner.invoke(app, ["ssh", "config", pi_name])
    assert result.exit_code == 0


def test_ssh_keys_count(pi_name):
    result = runner.invoke(app, ["ssh", "keys", "count", pi_name])
    assert result.exit_code == 0


def test_ssh_keys_show(pi_name):
    result = runner.invoke(app, ["ssh", "keys", "show", pi_name])
    assert result.exit_code == 0


def test_ssh_keys_list(pi_name):
    result = runner.invoke(app, ["ssh", "keys", "list", pi_name])
    assert result.exit_code == 0


def test_ssh_keys_table(pi_name):
    result = runner.invoke(app, ["ssh", "keys", "table", pi_name])
    assert result.exit_code == 0


def test_ssh_keys_add(ssh_key_path, pi_name):
    result = runner.invoke(app, ["ssh", "keys", "add", ssh_key_path, pi_name])
    assert result.exit_code == 0


def test_ssh_keys_copy(pi_name, random_pi_name):
    result = runner.invoke(app, ["ssh", "keys", "copy", pi_name, random_pi_name])
    assert result.exit_code == 0


def test_ssh_keys_remove(pi_name):
    result = runner.invoke(app, ["ssh", "keys", "remove", pi_name])
    assert result.exit_code == 0


def test_ssh_keys_purge(pi_name):
    result = runner.invoke(app, ["ssh", "keys", "purge", pi_name])
    assert result.exit_code == 0


def test_ssh_keys_import(pi_name):
    result = runner.invoke(app, ["ssh", "keys", "import", pi_name, "--github", "bennuttall"])
    assert result.exit_code == 0


def test_ssh_keys_unimport(pi_name):
    result = runner.invoke(app, ["ssh", "keys", "unimport", pi_name, "--github", "bennuttall"])
    assert result.exit_code == 0
