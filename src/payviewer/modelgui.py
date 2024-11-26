from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from enum import Enum
from enum import auto
from typing import TYPE_CHECKING

from guilib.dates.converters import date2days
from guilib.dates.converters import date2QDateTime
from guilib.dates.converters import days2date
from PySide6.QtCharts import QLineSeries

from payviewer.model import ColumnHeader
from payviewer.model import Info

if TYPE_CHECKING:
    from mypy_extensions import Arg
    from PySide6.QtCore import QDateTime


class SeriesModelUnit(Enum):
    EURO = auto()
    HOUR = auto()
    DAY = auto()


class UnknownColumnError(NotImplementedError):
    def __init__(self, info: Info, column_header: ColumnHeader) -> None:
        super().__init__(f'{info=}, {column_header=}')


@dataclass
class SeriesModel:
    series: list[QLineSeries]
    x_min: 'QDateTime'
    x_max: 'QDateTime'
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
    def ticket(cls, infos: list[Info]) -> 'SeriesModel':
        return SeriesModel._with_yearly_sum(
            SeriesModel._from_infos(
                infos, [ColumnHeader.ticket_pasto], SeriesModelUnit.EURO
            )
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
            x_min = min(when, x_min)
            x_max = max(when, x_max)
            for howmuch in howmuchs:
                y_min = min(howmuch, y_min)
                y_max = max(howmuch, y_max)

        return cls(
            series,
            date2QDateTime(x_min),
            date2QDateTime(x_max),
            float(y_min),
            float(y_max),
            unit,
        )

    @classmethod
    def _with_yearly_sum(cls, series_model: 'SeriesModel') -> 'SeriesModel':
        series = []
        for serie in series_model.series:
            series.append(serie)
            yearly_sum_serie = QLineSeries()
            yearly_sum_serie.setName(f'yearly sum for {serie.name()}')

            prev_year: None | int = None
            yearly_sum = 0.0
            for point in serie.points():
                when = days2date(point.x())
                if when.year != prev_year:
                    yearly_sum = 0.0
                    prev_year = when.year

                yearly_sum += point.y()
                yearly_sum_serie.append(date2days(when), float(yearly_sum))

            series.append(yearly_sum_serie)

        return cls(
            series,
            series_model.x_min,
            series_model.x_max,
            series_model.y_min,
            series_model.y_max,
            series_model.unit,
        )


SeriesModelFactory = Callable[[list[Info]], SeriesModel]
