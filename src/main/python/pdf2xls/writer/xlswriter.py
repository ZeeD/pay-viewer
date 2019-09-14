'xls writer'

import collections
import datetime
import decimal
import typing

import openpyxl

from . import abcwriter
from ..model import info
from ..model import keys

Table = typing.Dict[datetime.date, typing.Dict[str, decimal.Decimal]]


class XlsWriter(abcwriter.ABCWriter):
    'write infos on an .xls'

    def __init__(self, info_file: typing.BinaryIO) -> None:
        super().__init__(info_file)
        self.workbook = openpyxl.Workbook(write_only=True)
        self.sheet = self.workbook.create_sheet()
        self.sheet.append(['month'] + sorted(key.name for key in keys.Keys))
        self.table: Table = collections.defaultdict(dict)  # by month, then by key

    def write_feature_infos(self,
                            feature: keys.Keys,
                            infos: typing.Iterable[info.InfoPoint]) -> None:
        'keep track of the stuff to write'

        for info_point in infos:
            self.table[info_point.when][feature.name] = info_point.howmuch

    def close(self) -> None:
        'atomically write all the infos'

        for when in sorted(self.table):
            features: typing.Dict[str, decimal.Decimal] = self.table[when]

            row: typing.List[typing.Optional[typing.Union[decimal.Decimal, datetime.date]]] = []
            row += [when]
            row += [
                features[feature] if feature in features else None
                for feature in sorted(key.name for key in keys.Keys)
            ]

            self.sheet.append(row)

        self.workbook.save(typing.cast(typing.BinaryIO, self.info_file))
