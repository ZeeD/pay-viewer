import typing

import openpyxl.worksheet.worksheet

class Cell:
    number_format: str
    column_letter: str
    value: typing.Any

    def __init__(self,
                 worksheet: openpyxl.worksheet.worksheet.Worksheet,
                 value: typing.Any=None):
        ...
