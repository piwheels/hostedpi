import rich
from rich.console import Console
from rich.live import Live
from typer import Exit, Typer

from ..exc import HostedPiException
from . import arguments, options, utils
from .ssh import ssh_app


app = Typer(name="hostedpi", no_args_is_help=True)
app.add_typer(ssh_app, name="ssh", no_args_is_help=True, help="SSH access management commands")
console = Console()


@app.command("connect", hidden=True)
@app.command("test", help="Test a connection to the Mythic Beasts API")
def do_test():
    try:
        cloud = utils.get_picloud()
        cloud._auth.token
        utils.print_success("Connected to the Mythic Beasts API")
    except Exception:
        utils.print_error("Failed to authenticate")
        raise Exit(1)


@app.command("images")
def do_images(
    model: arguments.images_model,
    filter: options.filter_pattern_images = None,
):
    """
    List operating system images available for Raspberry Pi servers
    """
    cloud = utils.get_picloud()
    images = cloud.get_operating_systems(model=model)
    table = utils.make_table("ID", "Name")

    for id, name in sorted(images.items()):
        if filter is None or filter.lower() in id.lower() or filter.lower() in name.lower():
            table.add_row(id, name)
    rich.print(table)


@app.command("ls", hidden=True)
@app.command("list")
def do_list(
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
):
    """
    List Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)

    for pi in pis:
        print(pi.name)


@app.command("tab", hidden=True)
@app.command("table")
def do_table(
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
    full: options.full_table = False,
):
    """
    List Raspberry Pi server information in a table
    """
    pis = utils.get_pis(names, filter)

    if full:
        utils.full_pis_table(pis)
    else:
        utils.short_pis_table(pis)


@app.command("create")
def do_create(
    model: options.model,
    names: arguments.server_names = None,
    number: options.number = None,
    disk: options.disk_size = 10,
    memory: options.memory = None,
    cpu_speed: options.cpu_speed = None,
    os_image: options.os_image = None,
    wait: options.wait = False,
    ssh_key_path: options.ssh_key_path = None,
    ssh_import_github: options.ssh_import_github = None,
    ssh_import_launchpad: options.ssh_import_launchpad = None,
    full: options.full_table = False,
):
    """
    Provision one or more new Raspberry Pi servers
    """
    if names and number:
        utils.print_error("You can't specify both names and a number")
        raise Exit(1)
    if not names and not number:
        number = 1
    if full and not wait:
        utils.print_error("You can't use --full without --wait")
        raise Exit(1)
    if ssh_key_path is not None:
        if not ssh_key_path.exists():
            utils.print_error(f"SSH key file not found: {ssh_key_path}")
            raise Exit(1)
    ssh_import_gh_set = set(ssh_import_github) if ssh_import_github is not None else None
    ssh_import_lp_set = set(ssh_import_launchpad) if ssh_import_launchpad is not None else None

    if names:
        for name in names:
            try:
                utils.create_pi(
                    name=name,
                    model=model,
                    disk=disk,
                    memory_gb=memory,
                    cpu_speed=cpu_speed,
                    os_image=os_image,
                    wait=wait,
                    ssh_key_path=ssh_key_path,
                    github_usernames=ssh_import_gh_set,
                    launchpad_usernames=ssh_import_lp_set,
                    full=full,
                )
            except HostedPiException as exc:
                utils.print_exc(exc)
                continue

    if number:
        for n in range(number):
            try:
                utils.create_pi(
                    model=model,
                    disk=disk,
                    memory_gb=memory,
                    cpu_speed=cpu_speed,
                    os_image=os_image,
                    wait=wait,
                    ssh_key_path=ssh_key_path,
                    github_usernames=ssh_import_gh_set,
                    launchpad_usernames=ssh_import_lp_set,
                    full=full,
                )
            except HostedPiException as exc:
                utils.print_exc(exc)
                continue


@app.command("status")
def do_status(names: arguments.server_names = None, filter: options.filter_pattern_pi = None):
    """
    Get the current status of one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    table = utils.make_table("Name", "Status")
    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            try:
                table.add_row(pi.name, pi.status)
            except HostedPiException as exc:
                utils.print_exc(exc)
                table.add_row(pi.name, "Error")
                continue


@app.command("on")
def do_on(names: arguments.server_names = None, filter: options.filter_pattern_pi = None):
    """
    Power on one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    table = utils.make_table("Name", "Status")
    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            try:
                pi.on()
            except HostedPiException as exc:
                utils.print_exc(exc)
                table.add_row(pi.name, "Error")
                continue
            table.add_row(pi.name, "Powering on")


@app.command("off")
def do_off(names: arguments.server_names = None, filter: options.filter_pattern_pi = None):
    """
    Power off one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    table = utils.make_table("Name", "Status")
    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            try:
                pi.off()
            except HostedPiException as exc:
                utils.print_exc(exc)
                table.add_row(pi.name, "Error")
                continue
            table.add_row(pi.name, "Powering off")


@app.command("reboot")
def do_reboot(names: arguments.server_names = None, filter: options.filter_pattern_pi = None):
    """
    Reboot one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    table = utils.make_table("Name", "Status")
    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            try:
                pi.reboot()
            except HostedPiException as exc:
                utils.print_exc(exc)
                continue
            table.add_row(pi.name, "Rebooting")


@app.command("rm", hidden=True)
@app.command("cancel")
def do_cancel(
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
    yes: options.yes = False,
):
    """
    Unprovision one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    pis_str = ", ".join([pis.name for pis in pis])
    if len(pis) == 0:
        utils.print_error("No servers to cancel")
        raise Exit(1)
    if not yes:
        yn = input(f"Are you sure you want to cancel {pis_str}? [y/N] ")
        if yn.lower() != "y":
            raise Exit(1)
    table = utils.make_table("Name", "Status")
    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            try:
                pi.cancel()
            except HostedPiException as exc:
                table.add_row(pi.name, "Failed to cancel")
                utils.print_exc(exc)
                continue
            table.add_row(pi.name, "Cancelled")
