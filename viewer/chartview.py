from decimal import Decimal
from typing import List

from PySide6.QtCharts import QBarCategoryAxis
from PySide6.QtCharts import QBarSet
from PySide6.QtCharts import QChart
from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QStackedBarSeries
from PySide6.QtCore import QPointF, QObject, Slot
from PySide6.QtCore import Qt
from PySide6.QtCore import Signal
from PySide6.QtWidgets import QCheckBox
from PySide6.QtWidgets import QGraphicsSceneMouseEvent
from PySide6.QtWidgets import QGraphicsSceneWheelEvent
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QGroupBox
from PySide6.QtWidgets import QWidget

from .model import Rows


def new_bar_set(category: str, values: List[Decimal]) -> QBarSet:
    ret = QBarSet(category)
    ret.append(values)
    return ret


def build_series(rows: Rows, categories: list[str]) -> QStackedBarSeries:
    bar_sets = [new_bar_set(category,
                            [value.value
                             for row in rows
                             for value in row.values
                             if value.category == category])
                for category in categories]

    series = QStackedBarSeries()
    for bar_set in bar_sets:
        series.append(bar_set)
    return series


class Chart(QChart):
    def __init__(self, rows: Rows, categories: list[str]):
        super().__init__()

        series = build_series(rows, categories)
        self.addSeries(series)

        axis_x = QBarCategoryAxis()
        axis_x.append([row.date.isoformat() for row in rows])
        self.createDefaultAxes()
        self.setAxisX(axis_x, series)

        self.legend().setVisible(True)
        self.legend().setAlignment(Qt.AlignRight)
        self.legend().setShowToolTips(True)

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


class ChartView(QChartView):
    def __init__(self, parent: QWidget, rows: Rows, categories: list[str]):
        super().__init__(Chart(rows, categories), parent)
        self.rows = rows
        self.categories = categories

    def load(self, rows: Rows) -> None:
        self.setChart(Chart(rows, self.categories))
        self.rows = rows

    @Slot(list)
    def setCategories(self, categories: list[str]) -> None:
        self.setChart(Chart(self.rows, categories))
        self.categories = categories



class FilledGroupBox(QGroupBox):
    columns = 20
    categories_changed = Signal(list)

    def __init__(self, parent: QWidget, categories: list[str]):
        super().__init__(parent)

        layout = QGridLayout(self)

        row = -1
        for i, category in enumerate(categories):
            column = i % FilledGroupBox.columns
            if column == 0:
                row += 1
            checkbox = QCheckBox(category, self)
            checkbox.setChecked(True)
            checkbox.stateChanged.connect(self._trigger_categories_changed)
            layout.addWidget(checkbox, row, column)

        self.setLayout(layout)

    def _trigger_categories_changed(self, _: int) -> None:
        categories: list[str] = []

        layout: QGridLayout = self.layout()
        for row in range(layout.rowCount()):
            for column in range(layout.columnCount()):
                item = layout.itemAtPosition(row, column)
                if not item:
                    continue
                checkbox: QCheckBox = item.widget()
                if checkbox.isChecked():
                    categories.append(checkbox.text())

        self.categories_changed.emit(categories)