'stub for openpyxl'

import typing

import openpyxl.worksheet.worksheet
from pathlib import Path

class Workbook:

    def __init__(self, write_only: bool) -> None:
        '__init__'

    def create_sheet(self,
                     title: typing.Optional[str]=None
                     ) -> openpyxl.worksheet.worksheet.Worksheet:
        'create_sheet'

    def save(self, filename: Path) -> None:
        'save'
