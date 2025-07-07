from typing import Union


def memory(v: Union[int, None]) -> str:
    """
    Format memory size to GB
    """
    if v is None:
        return ""
    return f"{v} GB"


def cpu_speed(v: Union[int, None]) -> str:
    """
    Format CPU speed to GHz
    """
    if v is None:
        return ""
    return f"{v / 1000:.1f} GHz"


def nic_speed(v: Union[int, None]) -> str:
    """
    Format NIC speed to Mbps or Gbps
    """
    return {
        100: "100 Mbps",
        1000: "1 Gbps",
    }.get(v, "")


def disk_size(v: Union[int, None]) -> str:
    """
    Format disk size to GB or TB
    """
    if v is None:
        return ""
    if v < 1024:
        return f"{v} GB"
    return f"{v / 1024:.1f} TB"


def boolean(v: bool) -> str:
    """
    Format boolean to Yes or No
    """
    return "Yes" if v else "No"
