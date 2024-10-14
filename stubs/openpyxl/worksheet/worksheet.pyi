from collections.abc import Iterable
from typing import Any

from openpyxl.worksheet.dimensions import ColumnDimension

class Worksheet(list[Iterable[Any]]):
    column_dimensions: dict[str, ColumnDimension]
