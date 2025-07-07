from typer import Exit, Typer

from ..exc import HostedPiException
from . import arguments, options
from .sshkeys import keys_app
from .utils import get_pi, get_pis, print_error


ssh_app = Typer()
ssh_app.add_typer(keys_app, name="keys", no_args_is_help=True, help="SSH key management commands")


@ssh_app.command("command")
def do_command(name: arguments.server_name, ipv6: options.ipv6 = False):
    """
    Get the SSH command to connect to a Raspberry Pi server
    """
    pi = get_pi(name)
    if pi is None:
        print_error(f"Pi '{name}' not found")
        raise Exit(1)
    try:
        if ipv6:
            print(pi.ipv6_ssh_command)
        else:
            print(pi.ipv4_ssh_command)
    except HostedPiException as exc:
        print(f"hostedpi error: {exc}")
        raise Exit(1)


@ssh_app.command("config")
def do_config(
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
    ipv6: options.ipv6 = False,
):
    """
    Get the SSH config to connect to one or more Raspberry Pi servers
    """
    pis = get_pis(names, filter)
    for pi in pis:
        try:
            if ipv6:
                print(pi.ipv6_ssh_config)
            else:
                print(pi.ipv4_ssh_config)
        except HostedPiException as exc:
            print(f"hostedpi error: {exc}")
            raise Exit(1)
