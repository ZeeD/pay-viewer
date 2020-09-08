import typing

import openpyxl.worksheet.worksheet

class Cell:
    number_format: str

    def __init__(self,
                 worksheet: openpyxl.worksheet.worksheet.Worksheet,
                 value: typing.Any=None):
        ...
