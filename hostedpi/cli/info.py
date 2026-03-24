from typer import Typer

from . import arguments, format, options
from .utils import get_pi_or_exit


info_app = Typer()


@info_app.command("model")
def do_model(name: arguments.server_name, full: options.model_full = False):
    """
    Get the model of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    if full:
        print(pi.model_full)
    else:
        print(pi.model)


@info_app.command("memory")
def do_memory(name: arguments.server_name):
    """
    Get the memory of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(format.memory(pi.memory_gb))


@info_app.command("cpu")
def do_cpu_speed(name: arguments.server_name):
    """
    Get the CPU speed of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(format.cpu_speed(pi.cpu_speed))


@info_app.command("disk")
def do_disk_size(name: arguments.server_name):
    """
    Get the disk size of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(format.disk_size(pi.disk_size))


@info_app.command("nic")
def do_nic_speed(name: arguments.server_name):
    """
    Get the network interface speed of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(format.nic_speed(pi.nic_speed))


@info_app.command("status")
def do_status(name: arguments.server_name):
    """
    Get the current status of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(pi.status)


@info_app.command("boot-progress")
def do_boot_progress(name: arguments.server_name):
    """
    Get the boot progress of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(pi.boot_progress)


@info_app.command("ipv4-ssh-port")
def do_ipv4_ssh_port(name: arguments.server_name):
    """
    Get the IPv4 SSH port of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(pi.ipv4_ssh_port)


@info_app.command("ip-address")
def do_ip_address(name: arguments.server_name):
    """
    Get the IPv6 address of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(pi.ipv6_address.compressed)


@info_app.command("location")
def do_location(name: arguments.server_name):
    """
    Get the data centre location of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(pi.location)


@info_app.command("power")
def do_power(name: arguments.server_name):
    """
    Get the power state of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    print(pi.power)


@info_app.command("ssh-hostname")
def do_ssh_hostname(name: arguments.server_name, ipv6: options.ipv6 = False):
    """
    Get the SSH hostname of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    if ipv6:
        print(pi.ipv6_ssh_hostname)
    else:
        print(pi.ipv4_ssh_hostname)


@info_app.command("url")
def do_url(name: arguments.server_name, ssl: options.ssl = False):
    """
    Get the URL of a Raspberry Pi server
    """
    pi = get_pi_or_exit(name)
    if ssl:
        print(pi.url_ssl)
    else:
        print(pi.url)
