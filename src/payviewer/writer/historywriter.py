from json import dump
from typing import TYPE_CHECKING

from payviewer.writer.abcwriter import ABCWriter

if TYPE_CHECKING:
    from payviewer.model import AdditionalDetail
    from payviewer.model import Column
    from payviewer.model import Info
    from payviewer.reader.historyreader import RawAdditionalDetail
    from payviewer.reader.historyreader import RawColumn
    from payviewer.reader.historyreader import RawInfo


def _raw_column(column: 'Column') -> 'RawColumn':
    return {
        'header': column.header.name,
        'howmuch': (None if column.howmuch is None else str(column.howmuch)),
    }


def _raw_additional_details(
    additional_detail: 'AdditionalDetail',
) -> 'RawAdditionalDetail':
    return {
        'prev': additional_detail.prev,
        'fisc': additional_detail.fisc,
        'cod': additional_detail.cod,
        'descrizione': additional_detail.descrizione,
        'ore_o_giorni': str(additional_detail.ore_o_giorni),
        'compenso_unitario': str(additional_detail.compenso_unitario),
        'trattenute': str(additional_detail.trattenute),
        'competenze': str(additional_detail.competenze),
    }


def _raw_info(info: 'Info') -> 'RawInfo':
    return {
        'when': info.when.isoformat(),
        'columns': [_raw_column(column) for column in info.columns],
        'additional_details': [
            _raw_additional_details(additional_detail)
            for additional_detail in info.additional_details
        ],
    }


class HistoryWriter(ABCWriter):
    def write_infos(self, infos: list['Info']) -> None:
        with self.name.open('w', encoding='utf-8') as fp:
            dump([_raw_info(info) for info in infos], fp)
