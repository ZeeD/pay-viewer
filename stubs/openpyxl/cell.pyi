import typing

import openpyxl


class Cell:
    number_format: str

    def __init__(self, worksheet: openpyxl.Worksheet, value: typing.Any=None):
        ...
