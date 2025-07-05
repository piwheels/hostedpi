from pydantic import ValidationError
import pytest

from hostedpi.models.mythic.payloads import NewServer
from hostedpi.models.specs import Pi3ServerSpec


def test_bad_server_name():
    with pytest.raises(ValidationError):
        NewServer(name="bad name", spec=Pi3ServerSpec())


def test_empty_ssh_keys():
    server = NewServer(name="valid-name", spec=Pi3ServerSpec(), ssh_keys=set())
    assert server.ssh_keys is None
