from importlib.metadata import version
from functools import cache
from typing_extensions import Annotated

from typer import Typer, Argument
from rich import print
from rich.table import Table
from pydantic import ValidationError

from ..picloud import PiCloud
from .utils import make_table, validate_server_body
from .. import utils
from . import options, arguments, format
from ..exc import HostedPiException


hostedpi_version = version("hostedpi")


app = Typer(name="hostedpi", no_args_is_help=True)


@cache
def get_picloud() -> PiCloud:
    return PiCloud()


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
            str(data.data.model),
            format.memory(data.data.memory),
            format.cpu_speed(data.data.cpu_speed),
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
    wait_for_dns: options.wait_for_dns = False,
    wait_async: options.wait_async = False,
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
        "wait_for_dns": wait_for_dns,
    }
    data = {k: v for k, v in data.items() if v is not None}

    try:
        spec = validate_server_body(model, data)
    except ValidationError as exc:
        print(f"hostedpi error: {exc}")
        return 1

    try:
        pi = cloud.create_pi(name=name, spec=spec, wait_async=wait_async)
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
    cloud = get_picloud()
    pi = cloud.servers.get(name)
    table = Table("Name", pi.name)
    table.add_row("Model", pi.data.model_full)
    table.add_row("Memory", format.memory(pi.data.memory))
    table.add_row("CPU Speed", format.cpu_speed(pi.data.cpu_speed))
    table.add_row("NIC Speed", format.nic_speed(pi.data.nic_speed))
    table.add_row("Disk size", format.disk_size(pi.data.disk_size))
    print(table)


@app.command("rm", hidden=True)
@app.command("cancel")
def do_cancel(name: arguments.server_name):
    """
    Unprovision a Raspberry Pi server
    """
    cloud = get_picloud()
    pi = cloud.servers.get(name)
    try:
        pi.cancel()
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1
    print(f"Cancelled {name}")
