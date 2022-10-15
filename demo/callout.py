from PySide6.QtCharts import QChart, QLineSeries
from PySide6.QtCharts import QChartView
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtWidgets import QGraphicsProxyWidget
from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtWidgets import QLabel


class ChartHover(QGraphicsWidget):

    def __init__(self, parent: QGraphicsItem | None=None) -> None:
        super().__init__(parent)
        self.proxy = QGraphicsProxyWidget(self)

    def settext(self, text: str) -> None:
        self.proxy.setWidget(QLabel(text))


class Chart(QChart):

    def __init__(self) -> None:
        super().__init__()
        self.createDefaultAxes()

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
        self.setMouseTracking(True)

        self.hover = ChartHover(chart)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        pos = event.position()
        self.hover.settext(f'X: {pos.x():.2f} \nY: {pos.y():.2f} ')
        self.hover.setPos(pos)
        super().mouseMoveEvent(event)


app = QApplication([__file__])
v = ChartView()
v.show()
raise SystemExit(app.exec())
