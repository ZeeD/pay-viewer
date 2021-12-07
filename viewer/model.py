from csv import reader
from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import NamedTuple


class Value(NamedTuple):
    category: str
    value: Decimal


Values = list[Value]


class Row(NamedTuple):
    date: date
    values: Values


Rows = list[Row]


def loader(file_name: Path) -> Rows:
    with open(file_name, newline='', encoding='utf-8') as file:
        (_, *categories), *rows = reader(file)

    return [Row(date.fromisoformat(month),
                [Value(category, Decimal(value))
                 for (category, value) in zip(categories, values)
                 if value])
            for (month, *values) in rows]
