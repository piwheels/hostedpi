import rich
from rich.console import Console
from rich.live import Live
from rich.table import Table
from typer import Exit, Typer

from ..exc import HostedPiException
from ..utils import collect_ssh_keys, remove_imported_ssh_keys, remove_ssh_keys_by_label
from . import arguments, options, utils


keys_app = Typer()
console = Console()


@keys_app.command("count")
def do_count(names: arguments.server_names = None, filter: options.filter_pattern_pi = None):
    """
    Count the number of SSH keys on one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    table = utils.make_table("Name", "Keys")
    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            try:
                n = len(pi.ssh_keys)
            except HostedPiException as exc:
                utils.print_exc(exc)
                continue
            table.add_row(pi.name, str(n))


@keys_app.command("cat", hidden=True)
@keys_app.command("show")
def do_show(name: arguments.server_name):
    """
    List the SSH keys on a Raspberry Pi server as plaintext
    """
    pi = utils.get_pi(name)
    if pi is None:
        utils.print_error(f"Pi '{name}' not found")
        raise Exit(1)
    for key in pi.ssh_keys:
        try:
            print(key)
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue


@keys_app.command("list")
def do_list(name: arguments.server_name):
    """
    List the SSH keys on a Raspberry Pi server, using the key label and note if available
    """
    pi = utils.get_pi(name)
    if pi is None:
        utils.print_error(f"Pi '{name}' not found")
        raise Exit(1)
    keys = pi.ssh_keys
    if not keys:
        utils.print_warn(f"No SSH keys found on {pi.name}")
        return
    for key in keys:
        try:
            parts = key.split()
            print(" ".join(parts[2:]))
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue


@keys_app.command("table")
def do_table(name: arguments.server_name, filter: options.filter_pattern_pi = None):
    """
    List the SSH keys on a Raspberry Pi server in a table format
    """
    pi = utils.get_pi(name)
    if pi is None:
        utils.print_error(f"Pi '{name}' not found")
        raise Exit(1)
    headers = ["Type", "Label", "Note"]
    table = Table(*headers)

    for key in pi.ssh_keys:
        if filter and not filter.lower() in key.lower():
            continue
        label = ""
        note = ""
        parts = key.split(" ")
        key_type = parts[0]
        if len(parts) > 1:
            if "@" in parts[2]:
                label = parts[2]
                note = " ".join(parts[3:]).removeprefix("# ")
            else:
                note = " ".join(parts[2:]).removeprefix("# ")

        table.add_row(key_type, label, note)

    rich.print(table)


@keys_app.command("add")
def do_add(
    ssh_key_path: arguments.ssh_key_path,
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
):
    """
    Add an SSH key to one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    for pi in pis:
        keys_before = len(pi.ssh_keys)
        try:
            pi.ssh_keys |= {ssh_key_path.read_text()}
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        keys_after = len(pi.ssh_keys)
        if keys_after == keys_before:
            utils.print_warn(f"Key {ssh_key_path} already exists on {pi.name}")
        else:
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
            dest_pi.ssh_keys |= ssh_keys
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue

        num_keys_after = len(dest_pi.ssh_keys)
        num_keys_copied = num_keys_after - num_keys_before
        if num_keys_copied == 0:
            utils.print_warn(f"No new keys copied to {dest_pi.name} from {src_pi.name}")
        elif num_keys_copied == 1:
            utils.print_success(f"Copied 1 key from {src_pi.name} to {dest_pi.name}")
        else:
            utils.print_success(
                f"Copied {num_keys_copied} keys from {src_pi.name} to {dest_pi.name}"
            )


@keys_app.command("rm", hidden=True)
@keys_app.command("remove")
def do_remove(
    label: arguments.ssh_key_label,
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
):
    """
    Remove an SSH key from one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    for pi in pis:
        keys = pi.ssh_keys
        keys_before = len(keys)
        try:
            keys = remove_ssh_keys_by_label(keys, label)
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        pi.ssh_keys = keys
        removed_keys = keys_before - len(keys)
        if removed_keys == 0:
            utils.print_warn(f"No keys matching '{label}' found on {pi.name}")
        else:
            utils.print_success(f"Removed '{label}' key from {pi.name}")


@keys_app.command("purge")
def do_purge(names: arguments.server_names = None, filter: options.filter_pattern_pi = None):
    """
    Remove all SSH keys from one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    for pi in pis:
        keys = len(pi.ssh_keys)
        try:
            pi.ssh_keys = None
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        if keys == 0:
            utils.print_warn(f"No keys to remove from {pi.name}")
        elif keys == 1:
            utils.print_success(f"Removed 1 key from {pi.name}")
        else:
            utils.print_success(f"Removed {keys} keys from {pi.name}")


@keys_app.command("import")
def do_import(
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
    github: options.ssh_import_github = None,
    launchpad: options.ssh_import_launchpad = None,
):
    """
    Import SSH keys from GitHub and/or Launchpad to one or more Raspberry Pi servers
    """
    if not github and not launchpad:
        utils.print_error("You must specify at least one source to import from")
        raise Exit(1)
    pis = utils.get_pis(names, filter)
    ssh_keys = collect_ssh_keys(
        github_usernames=set(github) if github else None,
        launchpad_usernames=set(launchpad) if launchpad else None,
    )
    for pi in pis:
        keys_before = len(pi.ssh_keys)
        try:
            pi.ssh_keys |= ssh_keys
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        keys_after = len(pi.ssh_keys)
        keys_imported = keys_after - keys_before
        if keys_imported == 0:
            utils.print_warn(f"No new keys imported to {pi.name}")
        elif keys_imported == 1:
            utils.print_success(f"Imported 1 key to {pi.name}")
        else:
            utils.print_success(f"Imported {keys_imported} keys to {pi.name}")


@keys_app.command("unimport")
def do_unimport(
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
    github: options.ssh_import_github = None,
    launchpad: options.ssh_import_launchpad = None,
):
    """
    Remove imported SSH keys from one or more Raspberry Pi servers
    """
    if not github and not launchpad:
        utils.print_error("You must specify at least one source to unimport from")
        raise Exit(1)
    github = set(github) if github else set()
    launchpad = set(launchpad) if launchpad else set()
    pis = utils.get_pis(names, filter)
    for pi in pis:
        keys = pi.ssh_keys
        keys_before = len(keys)
        for gh_username in github:
            keys = remove_imported_ssh_keys(keys, "gh", gh_username)
        for lp_username in launchpad:
            keys = remove_imported_ssh_keys(keys, "lp", lp_username)
        try:
            pi.ssh_keys = keys
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        removed_keys = keys_before - len(keys)
        if removed_keys == 0:
            utils.print_warn(f"No keys matching import sources specified found on {pi.name}")
        elif removed_keys == 1:
            utils.print_success(f"Removed 1 key from {pi.name}")
        else:
            utils.print_success(f"Removed {removed_keys} keys from {pi.name}")
