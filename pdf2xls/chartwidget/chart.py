from datetime import date

from PySide6.QtCharts import QChart
from PySide6.QtCore import QRectF

from PySide6.QtCharts import QAbstractSeries


class Chart(QChart):
    def __init__(self) -> None:
        super().__init__()
        self.setAcceptHoverEvents(True)
        self.legend().hide()
        self._series: list[QAbstractSeries] = []

    def x_zoom(self, x_min: date, x_max: date, start_date: date) -> None:
        area = self.plotArea()
        old_x = area.x()
        y = area.y()
        old_w = area.width()
        h = area.height()

        w = old_w * (x_max - start_date) / (x_max - x_min)
        x = old_x + old_w - w

        self.zoomIn(QRectF(x, y, w, h))

    def replace_series(self, series: list[QAbstractSeries]) -> None:
        self.removeAllSeries()
        self._series.clear()
        for serie in series:
            self.addSeries(serie)
            self._series.append(serie)

    def series(self) -> list[QAbstractSeries]:
        return self._series
