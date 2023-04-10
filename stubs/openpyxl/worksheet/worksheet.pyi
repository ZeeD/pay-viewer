'stub for openpyxl'

from collections.abc import Iterable
from typing import Any

from .dimensions import ColumnDimension


class Worksheet(list[Iterable[Any]]):
    column_dimensions: dict[str, ColumnDimension]
