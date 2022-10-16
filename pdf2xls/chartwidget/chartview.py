from __future__ import annotations

from dataclasses import dataclass
from datetime import date
from decimal import Decimal
from typing import Optional
from typing import cast, Iterable

from PySide6.QtCharts import QAbstractSeries
from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QLineSeries
from PySide6.QtCharts import QValueAxis
from PySide6.QtCore import QDateTime, QPointF
from PySide6.QtCore import QPoint
from PySide6.QtCore import QRect
from PySide6.QtCore import QRectF
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtGui import QMouseEvent
from PySide6.QtGui import QPainter
from PySide6.QtGui import QPen
from PySide6.QtWidgets import QWidget

from ..model import ColumnHeader
from ..model import Info
from ..viewmodel import SortFilterViewModel
from ..viewmodel import ViewModel
from .chart import Chart
from .charthover import ChartHover
from .common import date2QDateTime
from .common import date2days
from .common import days2date
from .datetimeaxis import DateTimeAxis


@dataclass
class SeriesModel:
    series: list[QLineSeries]
    x_min: QDateTime
    x_max: QDateTime
    y_min: float
    y_max: float

    @classmethod
    def from_infos(cls, infos: list[Info]) -> SeriesModel:
        column_headers = [
            ColumnHeader.minimo,
            ColumnHeader.scatti,
            ColumnHeader.superm,
            ColumnHeader.sup_ass,
            ColumnHeader.edr,
            ColumnHeader.totale_retributivo,
            ColumnHeader.netto_da_pagare,
        ]
        series: list[QLineSeries] = []
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

        for info in sorted(infos, key=lambda info:info.when):
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

        return cls(series,
                   date2QDateTime(x_min), date2QDateTime(x_max),
                   float(y_min), float(y_max))


def tick_interval(y_max: float, n: int=10) -> float:
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
                 parent: Optional[QWidget]=None):
        super().__init__(parent)
        self.setMouseTracking(True)
        self._model = model.sourceModel()
        self._model.modelReset.connect(self.model_reset)  # type: ignore
        self._axis_x: Optional[DateTimeAxis] = None
        self._start_date: Optional[date] = None
        self._end_date: Optional[date] = None
        self.chart_hover = ChartHover()
        self.event_pos: Optional[QPointF] = None

    @Slot(date)
    def start_date_changed(self, start_date: date) -> None:
        self._start_date = start_date
        self._date_changed()

    @Slot(date)
    def end_date_changed(self, end_date: date) -> None:
        self._end_date = end_date
        self._date_changed()

    def _date_changed(self) -> None:
        chart = cast(Chart, self.chart())
        axis_x = self._axis_x
        if chart is None or axis_x is None:
            return

        start_date = self._start_date if self._start_date is not None else axis_x.min_date
        end_date = self._end_date if self._end_date is not None else axis_x.max_date
        chart.x_zoom(start_date, end_date)

    @Slot()
    def model_reset(self) -> None:
        series_model = SeriesModel.from_infos(self._model._infos)

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

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        chart = self.chart()
        if chart is not None:
            event_pos = event.position()
            event_value = chart.mapToValue(event_pos)

            # find closest x
            # assumption: all series have same x, so I can just one the first one
            series = cast(list[QLineSeries], chart.series())
            _, index, value = min(
                (abs(event_value.x() - point.x()), i, point)
                for i, point in enumerate(series[0].points())
            )

            for serie in series:
                serie.deselectAllPoints()
                serie.selectPoint(index)

            howmuchs = {'': Decimal(value.y())}
            for serie in series:
                howmuchs[serie.name()] = Decimal(f'{serie.at(index).y():.2f}')

            new_x = chart.mapToPosition(value).x()
            new_y = (self.size().height() - self.chart_hover.size().height()) / 2.
            self.event_pos = QPointF(new_x, new_y)

            self.chart_hover.set_howmuchs(howmuchs, self.event_pos)

        super().mouseMoveEvent(event)
        self.update()

    def drawForeground(self, painter: QPainter, rect: QRectF | QRect) -> None:
        super().drawForeground(painter, rect)
        if self.event_pos is not None:
            self.setUpdatesEnabled(False)
            try:
                painter.setPen(QPen(Qt.gray, 1, Qt.DashLine))
                x = self.event_pos.x()
                painter.drawLine(int(x), int(rect.top()),
                                 int(x), int(rect.bottom()))
            finally:
                self.setUpdatesEnabled(True)
