from decimal import Decimal

from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QLineSeries
from PySide6.QtCore import QObject
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication
from pdf2xls.chartwidget.chart import Chart
from pdf2xls.chartwidget.charthover import ChartHover


def serie(parent: QObject | None=None, points: list[tuple[float, float]]=[]) -> QLineSeries:
    ret = QLineSeries(parent)
    for x, y in points:
        ret.append(x, y)
    return ret


class ChartView(QChartView):

    def __init__(self) -> None:
        super().__init__()

        chart = Chart()
        chart.replace_series([
            serie(self, [(0, 3), (1, 5), (2, 4.5), (3, 1), (4, 2), (5, -3)]),
            serie(self, [(0, -1), (1, 0), (2, 2), (3, 0), (4, -1), (5, 0)]),
            serie(self, [(0, 0), (1, 0), (2, 0), (3, 0), (4, 0), (5, 0)]),
            serie(self, [(0, 10), (1, 10), (2, 10), (3, -10), (4, -10), (5, -10)]),
        ])
        chart.createDefaultAxes()

        self.setChart(chart)
        self.hover = ChartHover(chart)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        chart = self.chart()
        if not chart:
            raise Exception('no chart!')

        pos = event.position()
        value = chart.mapToValue(pos)

        howmuchs = {
            'x': Decimal.from_float(pos.x()),
            'y': Decimal.from_float(pos.y()),
            'ex': Decimal(value.x()),
            'ey': Decimal(value.y())
        }
        self.hover.set_howmuchs(howmuchs, pos)


app = QApplication([__file__])
v = ChartView()
v.show()
raise SystemExit(app.exec())
