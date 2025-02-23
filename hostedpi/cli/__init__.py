from typer import Typer
import rich

from . import options, arguments, utils
from .ssh import ssh_app
from ..exc import HostedPiException


app = Typer(name="hostedpi", no_args_is_help=True)
app.add_typer(ssh_app, name="ssh", no_args_is_help=True, help="SSH access management commands")


@app.command("connect", hidden=True)
@app.command("test", help="Test a connection to the Mythic Beasts API")
def do_test():
    try:
        cloud = utils.get_picloud()
        cloud._auth.token
        utils.print_success("Connected to the Mythic Beasts API")
    except Exception:
        utils.print_exc("Failed to authenticate")
        return 2


@app.command("images")
def do_images(
    model: arguments.images_model,
    filter: options.filter_pattern = None,
):
    """
    List operating system images available for Raspberry Pi servers
    """
    cloud = utils.get_picloud()
    images = cloud.get_operating_systems(model=model)
    table = utils.make_table("ID", "Name")

    for id, name in images.items():
        if filter is None or filter.lower() in id.lower() or filter.lower() in name.lower():
            table.add_row(id, name)
    rich.print(table)


@app.command("ls", hidden=True)
@app.command("list")
def do_list(
    names: arguments.server_names = None,
    filter: options.filter_pattern = None,
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
    filter: options.filter_pattern = None,
    full: options.full_table = False,
):
    """
    List Raspberry Pi server information in a table
    """
    pis = utils.get_pis(names, filter)

    if full:
        utils.full_table(pis)
    else:
        utils.short_table(pis)


@app.command(
    "create",
    short_help="Provision a new Raspberry Pi server",
    help="Provision a new Raspberry Pi server...",
)
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
    if names and number:
        utils.print_error("You can't specify both names and a number")
        return 1
    if not names and not number:
        number = 1
    if full and not wait:
        utils.print_error("You can't use --full without --wait")
    if ssh_key_path is not None:
        if not ssh_key_path.exists():
            utils.print_error(f"SSH key file not found: {ssh_key_path}")
            return 1
    if ssh_import_github is not None:
        ssh_import_github = set(ssh_import_github)
    if ssh_import_launchpad is not None:
        ssh_import_launchpad = set(ssh_import_launchpad)

    if names:
        for name in names:
            try:
                utils.create_pi(
                    name=name,
                    model=model,
                    disk=disk,
                    memory=memory,
                    cpu_speed=cpu_speed,
                    os_image=os_image,
                    wait=wait,
                    ssh_key_path=ssh_key_path,
                    ssh_import_github=ssh_import_github,
                    ssh_import_launchpad=ssh_import_launchpad,
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
                    memory=memory,
                    cpu_speed=cpu_speed,
                    os_image=os_image,
                    wait=wait,
                    ssh_key_path=ssh_key_path,
                    ssh_import_github=ssh_import_github,
                    ssh_import_launchpad=ssh_import_launchpad,
                    full=full,
                )
            except HostedPiException as exc:
                utils.print_exc(exc)
                continue


@app.command("status")
def do_status(names: arguments.server_names = None, filter: options.filter_pattern = None):
    """
    Get the current status of one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    for pi in pis:
        try:
            print(f"{pi.name}: {pi.status}")
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue


@app.command("on")
def do_on(names: arguments.server_names = None, filter: options.filter_pattern = None):
    """
    Power on one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    for pi in pis:
        try:
            pi.on()
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        utils.print_success(f"Powered on {pi.name}")


@app.command("off")
def do_off(names: arguments.server_names = None, filter: options.filter_pattern = None):
    """
    Power off one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    for pi in pis:
        try:
            pi.off()
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        utils.print_success(f"Powered off {pi.name}")


@app.command("reboot")
def do_reboot(names: arguments.server_names = None, filter: options.filter_pattern = None):
    """
    Reboot one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    for pi in pis:
        try:
            pi.reboot()
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        utils.print_success(f"Rebooted {pi.name}")


@app.command("rm", hidden=True)
@app.command("cancel")
def do_cancel(
    names: arguments.server_names = None,
    filter: options.filter_pattern = None,
    yes: options.yes = False,
):
    """
    Unprovision one or more Raspberry Pi servers
    """
    pis = utils.get_pis(names, filter)
    pis_str = ", ".join(pis)
    if len(pis) == 0:
        utils.print_error("No servers to cancel")
        return 1
    if not yes:
        yn = input(f"Are you sure you want to cancel {pis_str}? [y/N] ")
        if yn.lower() != "y":
            return 1
    for pi in pis:
        try:
            pi.cancel()
        except HostedPiException as exc:
            utils.print_exc(exc)
            continue
        utils.print_success(f"Cancelled {pi.name}")
