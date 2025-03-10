from datetime import date
from decimal import Decimal
from json import load
from typing import TYPE_CHECKING
from typing import TypedDict

from payviewer.model import AdditionalDetail
from payviewer.model import Column
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.reader.abcreader import ABCReader

if TYPE_CHECKING:
    from pathlib import Path


class RawColumn(TypedDict):
    header: str
    howmuch: str | None


class RawAdditionalDetail(TypedDict):
    prev: int | None
    fisc: int | None
    cod: int
    descrizione: str
    ore_o_giorni: str
    compenso_unitario: str
    trattenute: str
    competenze: str


class RawInfo(TypedDict):
    when: str
    columns: list[RawColumn]
    additional_details: list[RawAdditionalDetail]


def _column(raw_column: RawColumn) -> Column:
    return Column(
        header=ColumnHeader[raw_column['header']],
        howmuch=(
            None
            if raw_column['howmuch'] is None
            else Decimal(raw_column['howmuch'])
        ),
    )


def _additional_detail(
    raw_additional_detail: RawAdditionalDetail,
) -> AdditionalDetail:
    return AdditionalDetail(
        prev=raw_additional_detail['prev'],
        fisc=raw_additional_detail['fisc'],
        cod=raw_additional_detail['cod'],
        descrizione=raw_additional_detail['descrizione'],
        ore_o_giorni=Decimal(raw_additional_detail['ore_o_giorni']),
        compenso_unitario=Decimal(raw_additional_detail['compenso_unitario']),
        trattenute=Decimal(raw_additional_detail['trattenute']),
        competenze=Decimal(raw_additional_detail['competenze']),
    )


def _info(raw_info: RawInfo, path: 'Path') -> Info:
    return Info(
        when=date.fromisoformat(raw_info['when']),
        columns=[_column(raw_column) for raw_column in raw_info['columns']],
        additional_details=[
            _additional_detail(raw_additional_detail)
            for raw_additional_detail in raw_info['additional_details']
        ],
        path=path,
    )


class HistoryReader(ABCReader):
    def read_infos(self) -> list[Info]:
        with self.name.open(encoding='utf-8') as fp:
            return [_info(raw_info, self.name) for raw_info in load(fp)]
