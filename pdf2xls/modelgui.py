from __future__ import annotations

from collections.abc import Callable
from dataclasses import dataclass
from datetime import date
from decimal import Decimal

from mypy_extensions import Arg
from PySide6.QtCore import QDateTime
from qtpy.QtCharts import QLineSeries

from .dates import date2days
from .dates import date2QDateTime
from .model import ColumnHeader
from .model import Info


@dataclass
class SeriesModel:
    series: list[QLineSeries]
    x_min: QDateTime
    x_max: QDateTime
    y_min: float
    y_max: float

    @classmethod
    def money(cls, infos: list[Info]) -> SeriesModel:
        return SeriesModel._from_infos(infos, [
            ColumnHeader.minimo,
            ColumnHeader.scatti,
            ColumnHeader.superm,
            ColumnHeader.sup_ass,
            ColumnHeader.edr,
            ColumnHeader.totale_retributivo,
            ColumnHeader.netto_da_pagare,
        ])

    @classmethod
    def rol(cls, infos: list[Info]) -> SeriesModel:
        return SeriesModel._from_infos(infos, [
            ColumnHeader.par_a_prec,
            ColumnHeader.par_spett,
            ColumnHeader.par_godute,
            ColumnHeader.par_saldo,
            ColumnHeader.legenda_rol,
        ])

    @classmethod
    def ferie(cls, infos: list[Info]) -> SeriesModel:
        return SeriesModel._from_infos(infos, [
            ColumnHeader.ferie_a_prec,
            ColumnHeader.ferie_spett,
            ColumnHeader.ferie_godute,
            ColumnHeader.ferie_saldo,
            (ColumnHeader.legenda_ferie, lambda d:d/8),
        ])

    @classmethod
    def _from_infos(cls, infos: list[Info], column_headers: list[ColumnHeader | tuple[ColumnHeader, Callable[[Arg(Decimal, 'd')], Decimal]]]) -> SeriesModel:
        series: list[QLineSeries] = []
        for column_header in column_headers:
            if isinstance(column_header, ColumnHeader):
                pass
            else:
                column_header = column_header[0]
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
                        raise NotImplementedError(f'{info=}, {column_header=}')
                    return column.howmuch
            raise NotImplementedError(f'{info=}, {column_header=}')

        for info in sorted(infos, key=lambda info: info.when):
            when = info.when
            howmuchs = []
            for serie, column_header in zip(series, column_headers):
                if isinstance(column_header, ColumnHeader):
                    def op(d: Decimal)->Decimal: return d
                else:
                    column_header, op = column_header
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

        return cls(series,
                   date2QDateTime(x_min), date2QDateTime(x_max),
                   float(y_min), float(y_max))


SeriesModelFactory = Callable[[list[Info]], SeriesModel]
