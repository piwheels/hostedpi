from hostedpi.cli import format


def test_format_memory():
    assert format.memory(1) == "1 GB"
    assert format.memory(2) == "2 GB"
    assert format.memory(100) == "100 GB"
    assert format.memory(None) == ""


def test_format_cpu_speed():
    assert format.cpu_speed(1000) == "1.0 GHz"
    assert format.cpu_speed(1500) == "1.5 GHz"
    assert format.cpu_speed(2000) == "2.0 GHz"
    assert format.cpu_speed(20000) == "20.0 GHz"
    assert format.cpu_speed(None) == ""


def test_format_nic_speed():
    assert format.nic_speed(100) == "100 Mbps"
    assert format.nic_speed(1000) == "1 Gbps"
    assert format.nic_speed(None) == ""


def test_format_disk_size():
    assert format.disk_size(10) == "10 GB"
    assert format.disk_size(100) == "100 GB"
    assert format.disk_size(1000) == "1000 GB"
    assert format.disk_size(1500) == "1.5 TB"
    assert format.disk_size(20000) == "19.5 TB"
    assert format.disk_size(None) == ""


def test_format_boolean():
    assert format.boolean(True) == "Yes"
    assert format.boolean(False) == "No"
