from typer import Typer
import rich
from rich.live import Live
from rich.console import Console

from .utils import get_pi, get_all_pis, make_table
from ..exc import HostedPiException
from . import arguments


keys_app = Typer()
console = Console()


@keys_app.command("count")
def do_count(name: arguments.server_name):
    """
    Count the number of SSH keys on a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        print(len(pi.ssh_keys))
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1


@keys_app.command("show")
def do_show(name: arguments.server_name):
    """
    List the SSH keys on a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        for key in pi.ssh_keys:
            print(key)
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1


@keys_app.command("cp", hidden=True)
@keys_app.command("copy")
def do_copy(src: arguments.server_name, dest: arguments.server_name):
    """
    Copy the SSH keys from one Raspberry Pi server to another
    """
    src_pi = get_pi(src)
    dest_pi = get_pi(src)
    ssh_keys = src_pi.ssh_keys
    print(type(ssh_keys), len(ssh_keys))
    num_keys_before = len(dest_pi.ssh_keys)

    try:
        dest_pi.ssh_keys = ssh_keys
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1

    num_keys_after = len(dest_pi.ssh_keys)
    num_keys_copied = num_keys_after - num_keys_before
    print(f"Copied {num_keys_copied} keys from {src} to {dest}")


@keys_app.command("rm", hidden=True)
@keys_app.command("remove")
def do_remove(name: arguments.server_name):
    """
    Remove the SSH keys on a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        pi.ssh_keys = None
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1


@keys_app.command("add")
def do_add(name: arguments.server_name, ssh_key_path: arguments.ssh_key_path):
    """
    Add an SSH key to a Raspberry Pi server
    """
    pi = get_pi(name)
    try:
        pi.ssh_keys = {ssh_key_path.read_text()}
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        return 1
    print(f"Added key {ssh_key_path} to {name}")


@keys_app.command("table")
def do_table(names: arguments.server_names_optional = None):
    """
    Display the number of SSH keys on a Raspberry Pi server as a table
    """
    table = make_table("Name", "Keys")
    with Live(table, console=console, refresh_per_second=4):
        if names is None:
            names = get_all_pis()
        for name in sorted(names):
            pi = get_pi(name)
            table.add_row(name, str(len(pi.ssh_keys)))
        rich.print(table)
