'stub for openpyxl'

import typing

from .dimensions import ColumnDimension

class Worksheet(typing.List[typing.Iterable[typing.Any]]):
    column_dimensions: typing.Dict[str, ColumnDimension]
