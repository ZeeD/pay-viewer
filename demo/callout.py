from decimal import Decimal
from typing import cast

from PySide6.QtCharts import QChart, QLineSeries
from PySide6.QtCharts import QChartView
from PySide6.QtCore import Qt
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtWidgets import QGraphicsLayoutItem
from PySide6.QtWidgets import QGraphicsLinearLayout
from PySide6.QtWidgets import QGraphicsProxyWidget
from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtWidgets import QLabel


class ChartHover(QGraphicsWidget):

    def __init__(self, parent: QGraphicsItem | None=None) -> None:
        super().__init__(parent)
        self.items: list[QGraphicsLayoutItem] = []
        self.setLayout(QGraphicsLinearLayout(Qt.Vertical))

    def set_howmuchs(self, howmuchs: dict[str, Decimal]) -> None:
        layout = cast(QGraphicsLinearLayout, self.layout())
        for item in self.items:
            layout.removeItem(item)
        self.items.clear()
        for name, howmuch in howmuchs.items():
            item = QGraphicsProxyWidget(self)
            item.setWidget(QLabel(f'{name}: {howmuch}'))
            layout.addItem(item)
            self.items.append(item)


class Chart(QChart):

    def __init__(self) -> None:
        super().__init__()
        self.createDefaultAxes()
        self.legend().hide()

        series = QLineSeries(self)
        series.append(1, 3)
        series.append(4, 5)
        series.append(5, 4.5)
        series.append(7, 1)
        series.append(11, 2)
        self.addSeries(series)


class ChartView(QChartView):

    def __init__(self) -> None:
        super().__init__()

        chart = Chart()
        self.setChart(chart)
        self.hover = ChartHover(chart)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        chart = self.chart()
        if not chart:
            raise Exception('no chart!')
        pos = event.position()
        value = chart.mapToValue(pos)
        self.hover.set_howmuchs({
            'x': Decimal.from_float(pos.x()),
            'y': Decimal.from_float(pos.y()),
            'ex': Decimal(value.x()),
            'ey': Decimal(value.y())
        })
        self.hover.setPos(pos)
        super().mouseMoveEvent(event)


app = QApplication([__file__])
v = ChartView()
v.show()
raise SystemExit(app.exec())
