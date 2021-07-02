from csv import DictWriter
from datetime import date
from decimal import Decimal
from typing import Dict
from typing import Final
from typing import List
from typing import Union

from ..model import ColumnHeader
from ..model import Info
from .abcwriter import ABCWriter

MONTH: Final = 'month'


def fieldnames(infos: List[Info]) -> List[str]:
    return ([MONTH] +
            [column_header.name
             for column_header in ColumnHeader
             if column_header is not ColumnHeader.detail] +
            list(sorted({ad.descrizione
                         for info in infos
                         for ad in info.additional_details})))


def rows(infos: List[Info]) -> List[Dict[str, Union[date, Decimal]]]:
    return [{**{MONTH: info.when},
             **{c.header.name: c.howmuch
                for c in info.columns
                if c.howmuch is not None},
             **{ad.descrizione: ad.competenze - ad.trattenute
                for ad in info.additional_details}}
            for info in infos]


class CsvWriter(ABCWriter):
    def write_infos(self, infos: List[Info]) -> None:
        with open(self.name, 'w', newline='') as file:
            writer = DictWriter(file, fieldnames=fieldnames(infos))
            writer.writeheader()
            writer.writerows(rows(infos))
