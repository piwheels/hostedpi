from typing import Literal, Union
from functools import cache
from pathlib import Path

import rich
from rich.live import Live
from rich.console import Console
from rich.table import Table
from structlog import get_logger
from pydantic import ValidationError

from ..models.specs import Pi3ServerSpec, Pi4ServerSpec
from ..picloud import PiCloud
from ..pi import Pi
from ..exc import HostedPiException
from . import format
from ..models.sshkeys import SSHKeySources


logger = get_logger()
console = Console()


def make_table(*headers: str) -> Table:
    table = Table(show_header=True)
    for header in headers:
        table.add_column(header)
    return table


def validate_server_spec(model: Literal[3, 4], data: dict) -> Union[Pi3ServerSpec, Pi4ServerSpec]:
    if model == 3:
        return Pi3ServerSpec.model_validate(data)
    return Pi4ServerSpec.model_validate(data)


@cache
def get_picloud() -> PiCloud:
    return PiCloud()


def get_pi(name: str) -> Pi:
    cloud = get_picloud()
    try:
        return cloud.pis[name]
    except KeyError:
        raise HostedPiException(f"Pi not found: {name}")


def get_all_pis() -> list[Pi]:
    cloud = get_picloud()
    return list(cloud.pis.values())


def get_pis(names: Union[list[str], None], filter: Union[str, None] = None) -> list[Pi]:
    all_pis = get_all_pis()
    if not names:
        return filter_pis(all_pis, filter)
    all_pi_names = {pi.name for pi in all_pis}
    pis_not_found = [name for name in names if name not in all_pi_names]
    for pi in pis_not_found:
        logger.warn("Pi server not found", name=pi)
    pis_found = [pi for pi in all_pis if pi.name in names]
    return filter_pis(pis_found, filter)


def filter_pis(pis: list[Pi], filter: Union[str, None]) -> list[Pi]:
    return [pi for pi in pis if filter is None or filter.lower() in pi.name.lower()]


def short_pis_table(pis: list[Pi]):
    table = make_table("Name", "Model", "Memory", "CPU Speed")

    for pi in pis:
        table.add_row(
            pi.name,
            str(pi.model),
            format.memory(pi.memory),
            format.cpu_speed(pi.cpu_speed),
        )
    rich.print(table)


def full_pis_table(pis: list[Pi]):
    headers = [
        "Name",
        "Model",
        "Memory",
        "CPU Speed",
        "NIC Speed",
        "Disk size",
        "Status",
        "Initialised keys",
        "IPv4 SSH port",
    ]
    table = Table(*headers)

    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            table.add_row(
                pi.name,
                pi.model_full,
                format.memory(pi.memory),
                format.cpu_speed(pi.cpu_speed),
                format.nic_speed(pi.nic_speed),
                format.disk_size(pi.disk_size),
                pi.status,
                format.boolean(pi.initialised_keys),
                str(pi.ipv4_ssh_port),
            )


def create_pi(
    *,
    model: int,
    disk: int,
    memory: Union[int, None],
    cpu_speed: Union[int, None],
    os_image: Union[str, None],
    wait: bool,
    ssh_key_path: Union[Path, None],
    github_usernames: Union[set[str], None],
    launchpad_usernames: Union[set[str], None],
    full: bool,
    name: Union[str, None] = None,
):
    data = {
        "disk": disk,
        "memory": memory,
        "cpu_speed": cpu_speed,
        "os_image": os_image,
    }
    data = {k: v for k, v in data.items() if v is not None}

    ssh_keys = SSHKeySources(
        ssh_key_path=ssh_key_path,
        github_usernames=github_usernames,
        launchpad_usernames=launchpad_usernames,
    )

    try:
        spec = validate_server_spec(model, data)
    except ValidationError as exc:
        raise HostedPiException(f"Invalid server spec: {exc}") from exc

    cloud = get_picloud()
    pi = cloud.create_pi(name=name, spec=spec, ssh_keys=ssh_keys, wait=wait)

    if full:
        print_success("Server provisioned")
        full_pis_table([pi])
    elif wait:
        print_success("Server provisioned")
        short_pis_table([pi])
    else:
        print_success("Server provision request accepted")


def extract_ssh_key_label(key: str) -> Union[str, None]:
    parts = key.split(" ")
    if len(parts) > 2 and "@" in parts[2]:
        return parts[2]


def is_imported_ssh_key(key: str, source: Literal["gh", "lp"], username: str) -> bool:
    import_comment = f"{source}:{username}"
    return import_comment in key


def remove_ssh_keys_by_label(ssh_keys: set[str], label: str) -> set[str]:
    if label:
        return {key for key in ssh_keys if extract_ssh_key_label(key) != label}
    return ssh_keys


def remove_imported_ssh_keys(
    ssh_keys: set[str], source: Literal["gh", "lp"], username: str
) -> set[str]:
    return {key for key in ssh_keys if not is_imported_ssh_key(key, source, username)}


def print_exc(exc: Exception):
    logger.error(f"hostedpi error: {exc}")
    logger.debug("", exc_info=exc)


def print_error(error: str):
    console.print(f"[red]{error}[/red]")


def print_success(message: str):
    console.print(f"[green]{message}[/green]")


def print_warn(message: str):
    console.print(f"[yellow]{message}[/yellow]")
