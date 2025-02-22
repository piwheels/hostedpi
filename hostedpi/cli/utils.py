from typing import Literal, Union
from functools import cache
from pathlib import Path

import rich
from rich.live import Live
from rich.console import Console
from rich.table import Table
from structlog import get_logger
from pydantic import ValidationError

from ..models.payloads import NewPi3ServerBody, NewPi4ServerBody
from ..picloud import PiCloud
from ..pi import Pi
from ..exc import HostedPiException
from . import format


logger = get_logger()
console = Console()


def make_table(*headers: str) -> Table:
    table = Table(show_header=True)
    for header in headers:
        table.add_column(header)
    return table


def validate_server_body(model: Literal[3, 4], data: dict) -> NewPi3ServerBody | NewPi4ServerBody:
    if model == 3:
        return NewPi3ServerBody.model_validate(data)
    else:
        return NewPi4ServerBody.model_validate(data)


@cache
def get_picloud() -> PiCloud:
    return PiCloud()


def get_pi(name: str) -> Pi:
    cloud = get_picloud()
    try:
        return cloud.servers[name]
    except KeyError:
        raise HostedPiException(f"Pi not found: {name}")


def get_all_pis() -> dict[str, Pi]:
    cloud = get_picloud()
    return cloud.servers


def get_pis(names: list[str] | None) -> dict[str, Pi]:
    all_pis = get_all_pis()
    if not names:
        return all_pis
    pis_not_found = sorted(set(names) - set(all_pis))
    for pi in pis_not_found:
        logger.warn("Pi server not found", name=pi)
    return {name: pi for name, pi in all_pis.items() if name in names}


def short_table(names: Union[list[str], None]):
    pis = get_pis(names)
    table = make_table("Name", "Model", "Memory", "CPU Speed")

    for name, pi in sorted(pis.items()):
        table.add_row(
            name,
            str(pi.model),
            format.memory(pi.memory),
            format.cpu_speed(pi.cpu_speed),
        )
    rich.print(table)


def full_table(names: Union[list[str], None]):
    pis = get_pis(names)
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
        for name, pi in pis.items():
            table.add_row(
                name,
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
    model: int,
    disk: int,
    memory: int,
    cpu_speed: int,
    os_image: str,
    wait: bool,
    ssh_key_path: Union[Path, None],
    full: bool,
    *,
    name: str | None = None,
):
    cloud = get_picloud()

    data = {
        "disk": disk,
        "ssh_key": ssh_key_path.read_text() if ssh_key_path else None,
        "model": model,
        "memory": memory,
        "cpu_speed": cpu_speed,
        "os_image": os_image,
    }
    data = {k: v for k, v in data.items() if v is not None}

    try:
        spec = validate_server_body(model, data)
    except ValidationError as exc:
        raise HostedPiException(f"Invalid server spec: {exc}") from exc

    pi = cloud.create_pi(name=name, spec=spec, wait=wait)

    if full:
        full_table(names=[pi.name])
    elif wait:
        short_table(names=[pi.name])
    else:
        print_success("Server creation request accepted")


def print_exc(exc: Exception):
    logger.debug("hostedpi error", exc_info=exc)
    console.print(f"[red]hostedpi error: {exc}[/red]")


def print_error(error: str):
    console.print(f"[red]{error}[/red]")


def print_success(message: str):
    console.print(f"[green]{message}[/green]")
