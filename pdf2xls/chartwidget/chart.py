from datetime import date

from PySide6.QtCharts import QChart
from PySide6.QtCore import QRectF

from PySide6.QtCharts import QAbstractSeries


class Chart(QChart):
    def x_zoom(self, x_min: date, x_max: date, start_date: date) -> None:
        self.zoomReset()

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
        for serie in series:
            self.addSeries(serie)
