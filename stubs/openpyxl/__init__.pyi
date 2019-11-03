'stub for openpyxl'

import typing

Worksheet = typing.List[typing.Iterable[typing.Any]]


class Workbook:

    def __init__(self, write_only: bool) -> None:
        '__init__'

    def create_sheet(self,
                     title: typing.Optional[str]=None
                     ) -> Worksheet:
        'create_sheet'

    def save(self, info_file: typing.BinaryIO) -> None:
        'save'
