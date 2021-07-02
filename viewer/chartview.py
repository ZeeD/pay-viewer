from decimal import Decimal
from typing import List

from PySide2.QtCharts import QtCharts
from PySide2.QtCore import QPointF
from PySide2.QtCore import Qt
from PySide2.QtWidgets import QGraphicsSceneMouseEvent
from PySide2.QtWidgets import QGraphicsSceneWheelEvent
from PySide2.QtWidgets import QWidget

from .model import Rows


def new_bar_set(category: str, values: List[Decimal]) -> QtCharts.QBarSet:
    ret = QtCharts.QBarSet(category)
    ret.append(values)
    return ret


def build_series(rows: Rows) -> QtCharts.QStackedBarSeries:
    categories = list(sorted({value.category
                              for row in rows
                              for value in row.values}))

    bar_sets = [new_bar_set(category,
                            [value.value
                             for row in rows
                             for value in row.values
                             if value.category == category])
                for category in categories]

    series = QtCharts.QStackedBarSeries()
    for bar_set in bar_sets:
        series.append(bar_set)
    return series


class Chart(QtCharts.QChart):
    def __init__(self, rows: Rows):
        super().__init__()

        series = build_series(rows)
        self.addSeries(series)

        axis_x = QtCharts.QBarCategoryAxis()
        axis_x.append([row.date.isoformat() for row in rows])
        self.createDefaultAxes()
        self.setAxisX(axis_x, series)

        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignBottom)

    def wheelEvent(self, event: QGraphicsSceneWheelEvent) -> None:
        super().wheelEvent(event)

        y = event.delta()
        center_x = event.pos().x() - self.plotArea().x()

        if y < 0:
            self.zoom_x(.75, center_x)
        elif y > 0:
            self.zoom_x(2, center_x)

    def zoom_x(self, factor: float, center_x: float) -> None:
        rect = self.plotArea()
        rect_width = rect.width()

        rect.setWidth(rect_width / factor)
        rect.moveLeft(rect.x() + center_x -
                      (rect.width() * (center_x / rect_width)))

        self.zoomIn(rect)

    def mousePressEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mousePressEvent(event)
        event.accept()

    def mouseMoveEvent(self, event: QGraphicsSceneMouseEvent) -> None:
        super().mouseMoveEvent(event)

        def t(pos: QPointF) -> tuple[float, float]:
            return pos.x(), pos.y()

        x_curr, y_curr = t(event.pos())
        x_prev, y_prev = t(event.lastPos())
        self.scroll(x_prev - x_curr, y_curr - y_prev)


class ChartView(QtCharts.QChartView):
    def __init__(self, parent: QWidget, rows: Rows):
        super().__init__(Chart(rows), parent)

    def load(self, rows: Rows) -> None:
        self.setChart(Chart(rows))
