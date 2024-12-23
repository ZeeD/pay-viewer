from csv import DictWriter
from typing import TYPE_CHECKING
from typing import Final

from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.writer.abcwriter import ABCWriter

if TYPE_CHECKING:
    from datetime import date
    from decimal import Decimal

MONTH: Final = 'month'


def clean(descrizione: str) -> str:
    for prefix in (
        'AD.COM.LE DA TR. NEL ',
        'AD.REG.LE DA TR. NEL ',
        'TICKET PASTO',
    ):
        if descrizione.startswith(prefix):
            return f'{prefix}*'

    return descrizione


def fieldnames(infos: list[Info]) -> list[str]:
    return (
        [MONTH]
        + [
            column_header.name
            for column_header in ColumnHeader
            if column_header is not ColumnHeader.detail
        ]
        + sorted(
            {
                clean(ad.descrizione)
                for info in infos
                for ad in info.additional_details
            }
        )
    )


def rows(infos: list[Info]) -> list[dict[str, 'date | Decimal']]:
    return [
        {
            MONTH: info.when,
            **{
                c.header.name: c.howmuch
                for c in info.columns
                if c.howmuch is not None
            },
            **{
                clean(ad.descrizione): ad.competenze - ad.trattenute
                for ad in info.additional_details
            },
        }
        for info in infos
    ]


class CsvWriter(ABCWriter):
    def write_infos(self, infos: list[Info]) -> None:
        with self.name.open('w', newline='') as file:
            writer = DictWriter(file, fieldnames=fieldnames(infos))
            writer.writeheader()
            writer.writerows(rows(infos))
