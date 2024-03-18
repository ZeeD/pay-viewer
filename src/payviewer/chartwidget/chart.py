from typing import TYPE_CHECKING
from typing import cast

from qtpy.QtCharts import QAbstractSeries
from qtpy.QtCharts import QChart
from qtpy.QtCharts import QLineSeries
from qtpy.QtCore import Qt

from payviewer.dates import date2days

from .datetimeaxis import DateTimeAxis

if TYPE_CHECKING:
    from collections.abc import Iterable
    from datetime import date


class Chart(QChart):
    def __init__(self) -> None:
        super().__init__()
        self.setAcceptHoverEvents(True)
        self.legend().hide()
        self._series: list[QAbstractSeries] = []
        self.scrolledTo = 0.0

    def x_zoom(self, start_date: 'date', end_date: 'date') -> None:
        axis = cast(DateTimeAxis, self.axes(Qt.Orientation.Horizontal)[0])

        axis.setMin(date2days(start_date))
        axis.setMax(date2days(end_date))

    def replace_series(self, series: 'Iterable[QLineSeries]') -> None:
        self.removeAllSeries()
        self._series.clear()
        for serie in series:
            self.addSeries(serie)
            self._series.append(serie)

    def series(self) -> list[QAbstractSeries]:
        return self._series
