from typing import Literal
from functools import cache

from rich.table import Table

from ..models.payloads import NewPi3ServerBody, NewPi4ServerBody
from ..picloud import PiCloud
from ..pi import Pi
from ..exc import HostedPiException


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
