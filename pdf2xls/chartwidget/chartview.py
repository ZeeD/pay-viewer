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
from .chartslider import date2days
from .chartslider import days2date


@dataclass
class SeriesModel:
    series: QAbstractSeries
    x_min: QDateTime
    x_max: QDateTime
    y_min: float
    y_max: float


def date2QDateTime(d: date, *, epoch: date = date(1970, 1, 1)) -> QDateTime:
    return QDateTime.fromSecsSinceEpoch(int((d - epoch).total_seconds()))


def date2millis(d: date, *, epoch: date = date(1970, 1, 1)) -> float:
    return (d - epoch).total_seconds() * 1000


def series(infos: list[Info]) -> SeriesModel:
    series = QLineSeries()
    series.setName('netto_da_pagare')
    x_min = date.max
    x_max = date.min
    y_min = Decimal('inf')
    y_max = Decimal(0)

    # focus on netto_da_pagare column
    def netto_da_pagare(info: Info) -> Decimal:
        for column in info.columns:
            if column.header is ColumnHeader.netto_da_pagare:
                if column.howmuch is None:
                    raise NotImplementedError(f'{info}')
                return column.howmuch
        raise NotImplementedError(f'{info}')

    for info in infos:
        when = info.when
        howmuch = netto_da_pagare(info)

        series.append(date2days(when), float(howmuch))

        # update {x,y}_{min,max}
        if when < x_min:
            x_min = when
        if when > x_max:
            x_max = when
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

        # axis_x = QDateTimeAxis(self)
        # axis_x.setRange(series_model.x_min, series_model.x_max)
        # axis_x.setTickCount(8)
        axis_x = DateTimeAxis(series_model.x_min, series_model.x_max)
        chart.addAxis(axis_x, cast(Qt.Alignment, Qt.AlignBottom))
        series_model.series.attachAxis(axis_x)

        axis_y = QValueAxis(self)
        axis_y.setTickType(QValueAxis.TicksDynamic)
        axis_y.setTickAnchor(0.)
        axis_y.setMinorTickCount(9)
        axis_y.setTickInterval(tick_interval(series_model.y_max))
        chart.addAxis(axis_y, cast(Qt.Alignment, Qt.AlignLeft))
        series_model.series.attachAxis(axis_y)

        self.setChart(chart)
        self._axis_x = axis_x
