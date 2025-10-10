from typer import Exit, Typer

from ..exc import HostedPiException
from . import arguments, options
from .sshkeys import keys_app
from .utils import get_pi, get_pis, print_error


ssh_app = Typer()
ssh_app.add_typer(keys_app, name="keys", no_args_is_help=True, help="SSH key management commands")


@ssh_app.command("command")
def do_command(
    name: arguments.server_name,
    ipv6: options.ipv6 = False,
    numeric: options.numeric = False,
    user: options.user = "root",
):
    """
    Get the SSH command to connect to a Raspberry Pi server
    """
    if numeric and not ipv6:
        print_error("--numeric is only supported with --ipv6")
        raise Exit(1)

    pi = get_pi(name)
    if pi is None:
        print_error(f"Pi '{name}' not found")
        raise Exit(1)
    try:
        if ipv6:
            print(pi.get_ipv6_ssh_command(numeric=numeric, user=user))
        else:
            print(pi.get_ipv4_ssh_command(user=user))
    except HostedPiException as exc:
        print_error(f"hostedpi error: {exc}")
        raise Exit(1)


@ssh_app.command("config")
def do_config(
    names: arguments.server_names = None,
    filter: options.filter_pattern_pi = None,
    ipv6: options.ipv6 = False,
    numeric: options.numeric = False,
    user: options.user = "root",
):
    """
    Get the SSH config to connect to one or more Raspberry Pi servers
    """
    if numeric and not ipv6:
        print_error("--numeric is only supported with --ipv6")
        raise Exit(1)

    pis = get_pis(names, filter)
    for pi in pis:
        try:
            if ipv6:
                print(pi.get_ipv6_ssh_config(numeric=numeric, user=user))
            else:
                print(pi.get_ipv4_ssh_config(user=user))
        except HostedPiException as exc:
            print_error(f"hostedpi error: {exc}")
            raise Exit(1)
