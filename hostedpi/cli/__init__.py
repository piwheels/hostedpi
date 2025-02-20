from importlib.metadata import version
from functools import cache
from typing_extensions import Annotated

from typer import Typer, Argument
from rich import print
from rich.table import Table
from pydantic import ValidationError

from ..picloud import PiCloud
from ..pi import Pi
from .utils import make_table, validate_server_body
from .. import utils
from . import options, arguments, format
from ..exc import HostedPiException


hostedpi_version = version("hostedpi")


app = Typer(name="hostedpi", no_args_is_help=True)


@cache
def get_picloud() -> PiCloud:
    return PiCloud()


def get_pi(name: str) -> Pi:
    cloud = get_picloud()
    return cloud.servers.get(name)


@app.command("connect", hidden=True)
@app.command("test")
def do_test():
    """
    Test a connection to the Mythic Beasts API
    """
    try:
        cloud = get_picloud()
        cloud._auth.token
        print("Connected to the Mythic Beasts API")
    except Exception:
        print("Failed to authenticate")
        return 2


@app.command("images")
def do_images(
    model: Annotated[
        int, Argument(help="Model of Raspberry Pi server to list images for", min=3, max=4)
    ]
):
    """
    List operating system images available for Raspberry Pi servers
    """
    cloud = get_picloud()
    images = cloud.get_operating_systems(model=model)
    table = make_table("ID", "Name")
    for id, name in images.items():
        table.add_row(id, name)
    print(table)


@app.command("ls", hidden=True)
@app.command("list")
def do_list():
    """
    List Raspberry Pi servers
    """
    cloud = get_picloud()
    for name in sorted(cloud.servers):
        print(name)


@app.command("ll", hidden=True)
@app.command("table")
def do_table():
    """
    List Raspberry Pi servers in a table
    """
    cloud = get_picloud()
    table = make_table("Name", "Model", "Memory", "CPU Speed")
    for name, data in sorted(cloud.servers.items()):
        table.add_row(
            name,
            str(data.model),
            format.memory(data.memory),
            format.cpu_speed(data.cpu_speed),
        )
    print(table)


@app.command("create")
def do_create(
    model: arguments.model,
    name: options.server_name = None,
    disk: options.disk_size = 10,
    memory: options.memory = None,
    cpu_speed: options.cpu_speed = None,
    os_image: options.os_image = None,
    wait: options.wait_async = False,
    ssh_key_path: options.ssh_key_path = None,
):
    """
    Provision a new Raspberry Pi server
    """
    cloud = get_picloud()

    data = {
        "disk": disk,
        "ssh_key": utils.read_ssh_key(ssh_key_path) if ssh_key_path else None,
        "model": model,
        "memory": memory,
        "cpu_speed": cpu_speed,
        "os_image": os_image,
    }
    data = {k: v for k, v in data.items() if v is not None}

    try:
        spec = validate_server_body(model, data)
    except ValidationError as exc:
        print(f"hostedpi error: {exc}")
        return 1

    try:
        pi = cloud.create_pi(name=name, spec=spec, wait=wait)
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1

    if pi is not None:
        do_show_pi(name=pi.name)


@app.command("cat")
@app.command("show")
def do_show_pi(name: arguments.server_name):
    """
    Show details of a Raspberry Pi server
    """
    pi = get_pi(name)
    table = Table(pi.name)
    table.add_row("Model", pi.model_full)
    table.add_row("Memory", format.memory(pi.memory))
    table.add_row("CPU Speed", format.cpu_speed(pi.cpu_speed))
    table.add_row("NIC Speed", format.nic_speed(pi.nic_speed))
    table.add_row("Disk size", format.disk_size(pi.disk_size))
    table.add_row("Status", pi.status)
    table.add_row("Initialised keys", format.boolean(pi.disk_size))
    table.add_row("IPv4 SSH port", str(pi.disk_size))
    print(table)


@app.command("status")
def do_status(name: arguments.server_name):
    """
    Get the current status of a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        print(pi.status)
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1


@app.command("rm", hidden=True)
@app.command("cancel")
def do_cancel(name: arguments.server_name):
    """
    Unprovision a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        pi.cancel()
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1
    print(f"Cancelled {name}")


@app.command("on")
def do_on(name: arguments.server_name):
    """
    Power on a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        pi.on()
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1


@app.command("off")
def do_off(name: arguments.server_name):
    """
    Power off a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        pi.off()
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1


@app.command("reboot")
def do_reboot(name: arguments.server_name):
    """
    Reboot a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        pi.reboot()
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1


@app.command("ssh-command")
def do_ssh_command(name: arguments.server_name, ipv6: options.ipv6 = False):
    """
    Get the SSH command to connect to a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        if ipv6:
            print(pi.ipv6_ssh_command)
        else:
            print(pi.ipv4_ssh_command)
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1


@app.command("ssh-config")
def do_ssh_config(name: arguments.server_name, ipv6: options.ipv6 = False):
    """
    Get the SSH config to connect to a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        if ipv6:
            print(pi.ipv6_ssh_config)
        else:
            print(pi.ipv4_ssh_config)
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1
