from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import Iterator
from typing import NamedTuple

from pdf2xls.loader import load


class Value(NamedTuple):
    category: str
    value: Decimal


Values = list[Value]


class Row(NamedTuple):
    date: date
    values: Values


Rows = list[Row]


def loader(data_path: Path) -> Rows:
    def helper() -> Iterator[Row]:
        for info in load(str(data_path)):
            yield Row(date=info.when,
                      values=[Value(category=column.header.name,
                                    value=column.howmuch)
                              for column in info.columns
                              if column.howmuch is not None])
    return list(helper())
