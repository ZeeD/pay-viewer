from datetime import date
from typing import cast

from PySide6.QtCharts import QAbstractSeries, QLineSeries
from PySide6.QtCharts import QChart
from PySide6.QtCore import Qt

from .common import date2days
from .datetimeaxis import DateTimeAxis


class Chart(QChart):

    def __init__(self) -> None:
        super().__init__()
        self.setAcceptHoverEvents(True)
        self.legend().hide()
        self._series: list[QLineSeries] = []
        self.scrolledTo = 0.

    def x_zoom(self, start_date: date, end_date: date) -> None:
        axis = cast(DateTimeAxis, self.axes(Qt.Horizontal)[0])

        axis.setMin(date2days(start_date))
        axis.setMax(date2days(end_date))

    def replace_series(self, series: list[QLineSeries]) -> None:
        self.removeAllSeries()
        self._series.clear()
        for serie in series:
            self.addSeries(serie)
            self._series.append(serie)

    def series(self) -> list[QAbstractSeries]:
        return self._series
