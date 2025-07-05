from hostedpi.models.mythic.responses import PiInfoBasic, ServerSpec


def test_pi_info_basic():
    pi_info = PiInfoBasic(model=4, memory=2048, cpu_speed=1500)
    assert pi_info.model == 4
    assert pi_info.memory == 2048
    assert pi_info.cpu_speed == 1500
    assert pi_info.memory_gb == 2


def test_server_spec():
    spec = ServerSpec(disk=10, memory=2048, cpu_speed=1500, nic_speed=1500, model=4)
    assert spec.disk == 10
    assert spec.memory == 2048
    assert spec.cpu_speed == 1500
    assert spec.disk == 10
    assert spec.memory_gb == 2
    assert spec.nic_speed == 1500
    assert spec.model == 4
