from typing import Literal

from rich.table import Table

from hostedpi.models.payloads import NewPi3ServerBody, NewPi4ServerBody


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
