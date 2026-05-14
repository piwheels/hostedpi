from functools import cache
from pathlib import Path
from typing import Literal, Union

import rich
from typer import Exit
from pydantic import ValidationError
from rich.console import Console
from rich.live import Live
from rich.table import Table
from structlog import get_logger

from ..exc import HostedPiValidationError
from ..models.specs import Pi3ServerSpec, Pi4ServerSpec
from ..models.sshkeys import SSHKeySources
from ..pi import Pi
from ..picloud import PiCloud
from . import format

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


def get_pi(name: str) -> Union[Pi, None]:
    cloud = get_picloud()
    return cloud.pis.get(name)


def get_pi_or_exit(name: str) -> Pi:
    pi = get_pi(name)
    if pi is None:
        print_error("No server found with the given name.")
        raise Exit()
    return pi


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
        print_warn(f"Pi server not found: {pi}")
    pis_found = [pi for pi in all_pis if pi.name in names]
    return filter_pis(pis_found, filter)


def filter_pis(pis: list[Pi], filter: Union[str, None]) -> list[Pi]:
    return [pi for pi in pis if filter is None or filter.lower() in pi.name.lower()]


ALL_COLUMNS = [
    "model",
    "memory",
    "cpu",
    "disk",
    "nic",
    "status",
    "boot_progress",
    "ipv4_ssh_port",
    "ip_address",
    "location",
    "power",
]

COLUMN_DEFINITIONS = {
    "model": ("Model", lambda pi: pi.model_full),
    "memory": ("Memory", lambda pi: format.memory(pi.memory_gb)),
    "cpu": ("CPU Speed", lambda pi: format.cpu_speed(pi.cpu_speed)),
    "disk": ("Disk size", lambda pi: format.disk_size(pi.disk_size)),
    "nic": ("NIC Speed", lambda pi: format.nic_speed(pi.nic_speed)),
    "status": ("Status", lambda pi: pi.status),
    "boot_progress": ("Boot Progress", lambda pi: str(pi.boot_progress)),
    "ipv4_ssh_port": ("IPv4 SSH port", lambda pi: str(pi.ipv4_ssh_port)),
    "ip_address": ("IPv6 Address", lambda pi: pi.ipv6_address.compressed),
    "location": ("Location", lambda pi: pi.location),
    "power": ("Power", lambda pi: str(pi.power)),
}


def custom_pis_table(pis: list[Pi], columns: list[str]):
    headers = ["Name"] + [COLUMN_DEFINITIONS[col][0] for col in columns]
    table = make_table(*headers)
    with Live(table, console=console, refresh_per_second=4):
        for pi in pis:
            values = [pi.name] + [COLUMN_DEFINITIONS[col][1](pi) for col in columns]
            table.add_row(*values)


def short_pis_table(pis: list[Pi]):
    table = make_table("Name", "Model", "Memory", "CPU Speed")

    for pi in pis:
        table.add_row(
            pi.name,
            str(pi.model),
            format.memory(pi.memory_gb),
            format.cpu_speed(pi.cpu_speed),
        )
    rich.print(table)


def full_pis_table(pis: list[Pi]):
    custom_pis_table(pis, ALL_COLUMNS)


def create_pi(
    *,
    model: int,
    disk: int,
    memory_gb: Union[int, None],
    cpu_speed: Union[int, None],
    os_image: Union[str, None],
    wait: bool,
    ssh_key_path: Union[Path, None],
    github_usernames: Union[set[str], None],
    launchpad_usernames: Union[set[str], None],
    name: Union[str, None] = None,
) -> Pi:
    data = {
        "disk": disk,
        "memory_gb": memory_gb,
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
        raise HostedPiValidationError(f"Invalid server spec: {exc}") from exc

    cloud = get_picloud()
    return cloud.create_pi(name=name, spec=spec, ssh_keys=ssh_keys, wait=wait)


def print_exc(exc: Exception):
    logger.error(f"hostedpi error: {exc}")
    logger.debug("", exc_info=exc)


def print_error(error: str):
    console.print(f"[red]{error}[/red]")


def print_success(message: str):
    console.print(f"[green]{message}[/green]")


def print_warn(message: str):
    console.print(f"[yellow]{message}[/yellow]")
