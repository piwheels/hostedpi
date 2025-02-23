from typer import Typer
from rich.live import Live
from rich.console import Console

from . import utils
from ..exc import HostedPiException
from . import arguments, options
from ..utils import parse_ssh_keys


keys_app = Typer()
console = Console()


@keys_app.command("count")
def do_count(names: arguments.server_names = None):
    """
    Count the number of SSH keys on one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names)
    table = utils.make_table("Name", "Keys")
    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            try:
                n = len(pi.ssh_keys)
            except HostedPiException as exc:
                utils.print_exc(f"hostedpi error: {exc}")
                continue
            table.add_row(pi.name, str(n))


@keys_app.command("cat", hidden=True)
@keys_app.command("show")
def do_show(name: arguments.server_name):
    """
    List the SSH keys on a Raspberry Pi server
    """
    pi = utils.get_pi(name)
    for key in pi.ssh_keys:
        try:
            print(key)
        except HostedPiException as exc:
            utils.print_exc(f"hostedpi error: {exc}")
            continue


@keys_app.command("add")
def do_add(names: arguments.server_names, ssh_key_path: arguments.ssh_key_path):
    """
    Add an SSH key to a Raspberry Pi server
    """
    pis = utils.get_pis(names)
    for pi in pis:
        try:
            pi.ssh_keys = {ssh_key_path.read_text()}
        except HostedPiException as exc:
            utils.print_exc(f"hostedpi error: {exc}")
            continue
        utils.print_success(f"Added key {ssh_key_path} to {pi.name}")


@keys_app.command("cp", hidden=True)
@keys_app.command("copy")
def do_copy(src: arguments.server_name, dests: arguments.server_names):
    """
    Copy the SSH keys from one Raspberry Pi server to others
    """
    src_pi = utils.get_pi(src)
    dest_pis = utils.get_pis(dests)
    ssh_keys = src_pi.ssh_keys

    for dest_pi in dest_pis:
        num_keys_before = len(dest_pi.ssh_keys)

        try:
            dest_pi.ssh_keys = ssh_keys
        except HostedPiException as exc:
            utils.print_exc(f"hostedpi error: {exc}")
            continue

        num_keys_after = len(dest_pi.ssh_keys)
        num_keys_copied = num_keys_after - num_keys_before
        utils.print_success(f"Copied {num_keys_copied} keys from {src_pi.name} to {dest_pi.name}")


@keys_app.command("rm", hidden=True)
@keys_app.command("remove")
def do_remove(names: arguments.server_names):
    """
    Remove the SSH keys from one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names)
    for pi in pis:
        try:
            pi.ssh_keys = None
        except HostedPiException as exc:
            utils.print_exc(f"hostedpi error: {exc}")
            continue
        utils.print_success(f"Removed keys from {pi.name}")


@keys_app.command("import")
def do_import(
    names: arguments.server_names,
    github: options.ssh_import_github = None,
    launchpad: options.ssh_import_launchpad = None,
):
    """
    Import SSH keys from one or more files to one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names)
    ssh_keys = parse_ssh_keys(
        ssh_import_github=github,
        ssh_import_launchpad=launchpad,
    )
    for pi in pis:
        try:
            pi.ssh_keys = ssh_keys
        except HostedPiException as exc:
            utils.print_exc(f"hostedpi error: {exc}")
            continue
        utils.print_success(f"Imported {len(ssh_keys)} keys to {pi.name}")
