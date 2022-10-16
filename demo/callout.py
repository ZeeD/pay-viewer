from decimal import Decimal
from typing import cast
from typing import Iterable

from PySide6.QtCharts import QChartView
from PySide6.QtCharts import QLineSeries
from PySide6.QtCore import QObject
from PySide6.QtCore import QPointF
from PySide6.QtGui import QMouseEvent
from PySide6.QtWidgets import QApplication

from pdf2xls.chartwidget.chart import Chart
from pdf2xls.chartwidget.charthover import ChartHover


def serie(parent: QObject | None=None, points: Iterable[tuple[float, float]]=[]) -> QLineSeries:
    ret = QLineSeries(parent)
    for x, y in points:
        ret.append(x, y)
    return ret


class ChartView(QChartView):

    def __init__(self) -> None:
        super().__init__()

        chart = Chart()
        chart.replace_series([
            serie(self, zip(range(6), [ 3, 5, 4.5, 1, 2, -3])),
            serie(self, zip(range(6), [-1, 0, 2, 0, -1, 0])),
            serie(self, zip(range(6), [ 0, 0, 0, 0, 0, 0])),
            serie(self, zip(range(6), [10, 10, 10, -10, -10, -10])),
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

        # find closest x
        # assumption: all series have same x, so I can just one the first one
        series = cast(list[QLineSeries], chart.series())
        _, index, value = min(
            (abs(value.x() - point.x()), i, point)
            for i, point in enumerate(series[0].points())
        )

        for serie in series:
            serie.deselectAllPoints()
            serie.selectPoint(index)

        howmuchs = {
            'x': Decimal.from_float(pos.x()),
            'y': Decimal.from_float(pos.y()),
            'ex': Decimal(value.x()),
            'ey': Decimal(value.y())
        }

        new_x = chart.mapToPosition(value).x()
        new_y = (self.size().height() - self.hover.size().height()) / 2.
        new_pos = QPointF(new_x, new_y)

        self.hover.set_howmuchs(howmuchs, new_pos)


app = QApplication([__file__])
v = ChartView()
v.show()
raise SystemExit(app.exec())
