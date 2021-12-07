'stub for openpyxl'

from typing import Any
from typing import Iterable

from .dimensions import ColumnDimension


class Worksheet(list[Iterable[Any]]):
    column_dimensions: dict[str, ColumnDimension]
