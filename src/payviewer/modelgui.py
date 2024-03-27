from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from enum import auto
from os import environ
from typing import TYPE_CHECKING

from guilib.chartslider.chartslider import EPOCH
from guilib.chartslider.chartslider import date2days

from payviewer.model import ColumnHeader
from payviewer.model import Info

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCharts import QLineSeries
from qtpy.QtCore import QDateTime

if TYPE_CHECKING:
    from mypy_extensions import Arg


class SeriesModelUnit(Enum):
    EURO = auto()
    HOUR = auto()
    DAY = auto()


class UnknownColumnError(NotImplementedError):
    def __init__(self, info: Info, column_header: ColumnHeader) -> None:
        super().__init__(f'{info=}, {column_header=}')


def date2QDateTime(d: date, *, epoch: date = EPOCH) -> 'QDateTime':  # noqa: N802
    return QDateTime.fromSecsSinceEpoch(int((d - epoch).total_seconds()))


@dataclass
class SeriesModel:
    series: list[QLineSeries]
    x_min: QDateTime
    x_max: QDateTime
    y_min: float
    y_max: float
    unit: SeriesModelUnit

    @classmethod
    def money(cls, infos: list[Info]) -> 'SeriesModel':
        return SeriesModel._from_infos(
            infos,
            [
                ColumnHeader.minimo,
                ColumnHeader.scatti,
                ColumnHeader.superm,
                ColumnHeader.sup_ass,
                ColumnHeader.edr,
                ColumnHeader.totale_retributivo,
                ColumnHeader.netto_da_pagare,
            ],
            SeriesModelUnit.EURO,
        )

    @classmethod
    def rol(cls, infos: list[Info]) -> 'SeriesModel':
        return SeriesModel._from_infos(
            infos,
            [
                ColumnHeader.par_a_prec,
                ColumnHeader.par_spett,
                ColumnHeader.par_godute,
                ColumnHeader.par_saldo,
                ColumnHeader.legenda_rol,
            ],
            SeriesModelUnit.HOUR,
        )

    @classmethod
    def ferie(cls, infos: list[Info]) -> 'SeriesModel':
        return SeriesModel._from_infos(
            infos,
            [
                ColumnHeader.ferie_a_prec,
                ColumnHeader.ferie_spett,
                ColumnHeader.ferie_godute,
                ColumnHeader.ferie_saldo,
                (ColumnHeader.legenda_ferie, lambda d: d / 8),
            ],
            SeriesModelUnit.DAY,
        )

    @classmethod
    def _from_infos(  # noqa: C901
        cls,
        infos: list[Info],
        column_headers: list[
            ColumnHeader
            | tuple[ColumnHeader, "Callable[[Arg(Decimal, 'd')], Decimal]"]
        ],
        unit: SeriesModelUnit,
    ) -> 'SeriesModel':
        series: list[QLineSeries] = []
        for column_header_ in column_headers:
            column_header = (
                column_header_
                if isinstance(column_header_, ColumnHeader)
                else column_header_[0]
            )
            serie = QLineSeries()
            serie.setName(column_header.name)
            series.append(serie)

        x_min = date.max
        x_max = date.min
        y_min = Decimal('inf')
        y_max = Decimal(0)

        def get_howmuch(info: Info, column_header: ColumnHeader) -> Decimal:
            for column in info.columns:
                if column.header is column_header:
                    if column.howmuch is None:
                        raise UnknownColumnError(info, column_header)
                    return column.howmuch
            raise UnknownColumnError(info, column_header)

        for info in sorted(infos, key=lambda info: info.when):
            when = info.when
            howmuchs = []
            for serie, column_header_ in zip(
                series, column_headers, strict=False
            ):
                if isinstance(column_header_, ColumnHeader):
                    column_header = column_header_

                    def op(d: Decimal) -> Decimal:
                        return d
                else:
                    column_header, op = column_header_
                howmuch = op(get_howmuch(info, column_header))
                howmuchs.append(howmuch)
                serie.append(date2days(when), float(howmuch))

            # update {x,y}_{min,max}
            if when < x_min:
                x_min = when
            if when > x_max:
                x_max = when
            for howmuch in howmuchs:
                if howmuch < y_min:
                    y_min = howmuch
                if howmuch > y_max:
                    y_max = howmuch

        return cls(
            series,
            date2QDateTime(x_min),
            date2QDateTime(x_max),
            float(y_min),
            float(y_max),
            unit,
        )


SeriesModelFactory = Callable[[list[Info]], SeriesModel]
