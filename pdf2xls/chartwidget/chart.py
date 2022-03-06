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

    def x_zoom(self,
               x_min: date, x_max: date,
               start_date: date, end_date: date) -> None:
        area = self.plotArea()
        old_x = area.x()
        y = area.y()
        old_w = area.width()
        h = area.height()

        print(f'[{end_date}, {start_date}, {x_max}, {x_min}] [{end_date-start_date}, {x_max-x_min}]')

        w = old_w * (end_date - start_date) / (x_max - x_min)
        x = old_x + old_w - w

        print(f'{old_x:.2f} x {old_w:.2f}\n{x:.2f} x {w:.2f}\n')

        self.zoomIn(QRectF(x, y, w, h))

    def replace_series(self, series: list[QAbstractSeries]) -> None:
        self.removeAllSeries()
        self._series.clear()
        for serie in series:
            self.addSeries(serie)
            self._series.append(serie)

    def series(self) -> list[QAbstractSeries]:
        return self._series
