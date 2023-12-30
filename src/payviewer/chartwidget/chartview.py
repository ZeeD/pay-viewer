from __future__ import annotations

from datetime import date
from decimal import Decimal
from typing import TYPE_CHECKING
from typing import cast
from typing import override

from qtpy.QtCharts import QChartView
from qtpy.QtCharts import QLineSeries
from qtpy.QtCharts import QValueAxis
from qtpy.QtCore import QPointF
from qtpy.QtCore import QRect
from qtpy.QtCore import QRectF
from qtpy.QtCore import Qt
from qtpy.QtCore import Slot
from qtpy.QtGui import QMouseEvent
from qtpy.QtGui import QPainter
from qtpy.QtGui import QPen

from payviewer.dates import days2date

from .chart import Chart
from .charthover import ChartHover
from .datetimeaxis import DateTimeAxis

if TYPE_CHECKING:
    from qtpy.QtWidgets import QWidget

    from payviewer.modelgui import SeriesModelFactory
    from payviewer.viewmodel import SortFilterViewModel


def tick_interval(y_max: float, n: int = 10) -> float:
    "Return min(10**x) > y_max / n ."
    goal_step = y_max / n
    exp = 1
    while True:
        y_step = 10.0**exp
        if y_step > goal_step:
            return y_step
        exp += 1


class ChartView(QChartView):
    def __init__(
        self,
        model: SortFilterViewModel,
        parent: QWidget | None,
        factory: SeriesModelFactory,
    ) -> None:
        super().__init__(parent)
        self.setMouseTracking(True)  # noqa: FBT003
        self._model = model.sourceModel()
        self._model.modelReset.connect(self.model_reset)
        self._axis_x: DateTimeAxis | None = None
        self._start_date: date | None = None
        self._end_date: date | None = None
        self.chart_hover = ChartHover()
        self.event_pos: QPointF | None = None
        self.factory = factory

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

        start_date = (
            self._start_date
            if self._start_date is not None
            else axis_x.min_date
        )
        end_date = (
            self._end_date if self._end_date is not None else axis_x.max_date
        )
        chart.x_zoom(start_date, end_date)

    @Slot()
    def model_reset(self) -> None:
        series_model = self.factory(self._model._infos)  # noqa: SLF001

        chart = Chart()
        chart.replace_series(series_model.series)

        axis_x = DateTimeAxis(series_model.x_min, series_model.x_max)
        chart.addAxis(axis_x, Qt.AlignmentFlag.AlignBottom)
        for serie in series_model.series:
            serie.attachAxis(axis_x)

        axis_y = QValueAxis(self)
        chart.addAxis(axis_y, Qt.AlignmentFlag.AlignLeft)
        for serie in series_model.series:
            serie.attachAxis(axis_y)
        axis_y.setTickType(QValueAxis.TickType.TicksDynamic)
        axis_y.setTickAnchor(0.0)
        axis_y.setMinorTickCount(9)
        axis_y.setTickInterval(tick_interval(series_model.y_max))
        axis_y.setMin(series_model.y_min)
        axis_y.setMax(series_model.y_max)

        self.setChart(chart)
        self.chart_hover.setParentItem(chart)
        self._axis_x = axis_x

    @override
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

            when = days2date(value.x())

            howmuchs = {
                serie.name(): (
                    serie.color(),
                    Decimal(f'{serie.at(index).y(): .2f}'),
                )
                for serie in series
            }

            self.event_pos = chart.mapToPosition(value)

            new_x = self.event_pos.x()
            if new_x + self.chart_hover.size().width() > self.size().width():
                new_x -= self.chart_hover.size().width()
            new_y = 100

            self.chart_hover.set_howmuchs(when, howmuchs, QPointF(new_x, new_y))

        super().mouseMoveEvent(event)
        self.update()

    @override
    def drawForeground(self, painter: QPainter, rect: QRectF | QRect) -> None:
        super().drawForeground(painter, rect)
        if self.event_pos is None:
            return

        self.setUpdatesEnabled(False)  # noqa: FBT003
        try:
            painter.setPen(QPen(Qt.GlobalColor.gray, 1, Qt.PenStyle.DashLine))
            x = self.event_pos.x()
            painter.drawLine(
                int(x), int(rect.top()), int(x), int(rect.bottom())
            )
        finally:
            self.setUpdatesEnabled(True)  # noqa: FBT003
