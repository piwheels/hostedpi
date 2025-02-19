def memory(v: int) -> str:
    """
    Format memory size to GB
    """
    return f"{v / 1024:.0f} GB"


def cpu_speed(v: int) -> str:
    """
    Format CPU speed to GHz
    """
    return f"{v / 1000:.1f} GHz"


def nic_speed(v: int) -> str:
    """
    Format NIC speed to Mbps or Gbps
    """
    return {
        100: "100 Mbps",
        1000: "1 Gbps",
    }[v]


def disk_size(v: int) -> str:
    """
    Format disk size to GB or TB
    """
    if v < 1024:
        return f"{v} GB"
    return f"{v / 1024:.1f} TB"


def boolean(v: bool) -> str:
    """
    Format boolean to Yes or No
    """
    return "Yes" if v else "No"
