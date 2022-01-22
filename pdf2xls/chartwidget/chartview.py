from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import cast
from typing import Optional

from PySide6.QtCharts import QAbstractAxis
from PySide6.QtCharts import QAbstractSeries
from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QLineSeries
from PySide6.QtCharts import QValueAxis
from PySide6.QtCore import QDateTime
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from pdf2xls.chartwidget.datetimeaxis import DateTimeAxis
from pdf2xls.viewmodel import ViewModel

from ..model import ColumnHeader
from ..model import Info
from ..viewmodel import SortFilterViewModel
from .chart import Chart
from .common import date2days
from .common import date2QDateTime
from .common import days2date


@dataclass
class SeriesModel:
    series: list[QAbstractSeries]
    x_min: QDateTime
    x_max: QDateTime
    y_min: float
    y_max: float


def series(infos: list[Info]) -> SeriesModel:
    column_headers = [
        ColumnHeader.minimo,
        ColumnHeader.scatti,
        ColumnHeader.superm,
        ColumnHeader.sup_ass,
        ColumnHeader.edr,
        ColumnHeader.totale_retributivo,
        ColumnHeader.netto_da_pagare,
    ]
    series: list[QAbstractSeries] = []
    for column_header in column_headers:
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

    for info in infos:
        when = info.when
        howmuchs = []
        for serie, column_header in zip(series, column_headers):
            howmuch = get_howmuch(info, column_header)
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

    return SeriesModel(series,
                       date2QDateTime(x_min), date2QDateTime(x_max),
                       float(y_min), float(y_max))


def tick_interval(y_max: float, n: int = 10) -> float:
    'return min(10**x) > y_max / n'
    goal_step = y_max / n
    exp = 1
    while True:
        y_step = 10.**exp
        if y_step > goal_step:
            return y_step
        exp += 1


class ChartView(QChartView):
    def __init__(self,
                 model: SortFilterViewModel,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self._model: ViewModel = model.sourceModel()
        self._model.modelReset.connect(self.model_reset)
        self._axis_x: Optional[QAbstractAxis] = None

    @Slot(date)
    def start_date_changed(self, start_date: date) -> None:
        chart: Chart = self.chart()
        axis_x = self._axis_x
        if chart is None or axis_x is None:
            return

        x_min = days2date(axis_x.min())
        x_max = days2date(axis_x.max())
        chart.x_zoom(x_min, x_max, start_date)

    @Slot()
    def model_reset(self) -> None:
        series_model = series(self._model._infos)

        chart = Chart()
        chart.replace_series(series_model.series)

        axis_x = DateTimeAxis(series_model.x_min, series_model.x_max)
        chart.addAxis(axis_x, cast(Qt.Alignment, Qt.AlignBottom))
        for serie in series_model.series:
            serie.attachAxis(axis_x)

        axis_y = QValueAxis(self)
        chart.addAxis(axis_y, cast(Qt.Alignment, Qt.AlignLeft))
        for serie in series_model.series:
            serie.attachAxis(axis_y)
        axis_y.setTickType(QValueAxis.TicksDynamic)
        axis_y.setTickAnchor(0.)
        axis_y.setMinorTickCount(9)
        axis_y.setTickInterval(tick_interval(series_model.y_max))
        axis_y.setMin(series_model.y_min)
        axis_y.setMax(series_model.y_max)

        self.setChart(chart)
        self._axis_x = axis_x
