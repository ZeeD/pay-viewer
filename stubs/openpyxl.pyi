'stub for openpyxl'

import typing


class Workbook:

    def __init__(self, write_only: bool) -> None:
        '__init__'

    def create_sheet(self) -> typing.List[list]:
        'create_sheet'

    def save(self, info_file: typing.BinaryIO) -> None:
        'save'
