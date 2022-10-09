from typing import cast
from typing import Optional

from PySide6.QtCharts import QChart
from PySide6.QtCharts import QLineSeries
from PySide6.QtCore import QPointF
from PySide6.QtCore import QRect
from PySide6.QtCore import QRectF
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor, QMouseEvent
from PySide6.QtGui import QFont
from PySide6.QtGui import QFontMetrics
from PySide6.QtGui import QPainter
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtWidgets import QGraphicsScene
from PySide6.QtWidgets import QGraphicsView
from PySide6.QtWidgets import QStyleOptionGraphicsItem
from PySide6.QtWidgets import QWidget


class Callout(QGraphicsItem):

    def __init__(self, chart: QChart):
        super().__init__(chart)
        self.setZValue(11)
        self._boundingRect = QRectF()
        self.text = ''

    def boundingRect(self) -> QRectF:
        return self._boundingRect

    def paint(self, painter: QPainter, option: QStyleOptionGraphicsItem, widget: Optional[QWidget]=None) -> None:
        painter.setBrush(QColor(255, 255, 255))
        painter.drawText(self._boundingRect, self.text)

    def settext(self, text: str) -> None:
        self.text = text
        self._boundingRect = QRectF(QFontMetrics(QFont()).boundingRect(QRect(),
                                                                       cast(int, Qt.AlignLeft),
                                                                       text,
                                                                       0))


class View(QGraphicsView):

    def __init__(self) -> None:
        super().__init__()
        self.setMouseTracking(True)

        chart = QChart()
        chart.createDefaultAxes()
        chart.setAcceptHoverEvents(True)

        series = QLineSeries()
        series.append(1, 3)
        series.append(4, 5)
        series.append(5, 4.5)
        series.append(7, 1)
        series.append(11, 2)
        chart.addSeries(series)

        scene = QGraphicsScene(self)
        scene.addItem(chart)
        self.setScene(scene)

        self.callout = Callout(chart)
        self.chart = chart

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.scene().setSceneRect(QRectF(QPointF(0, 0), event.size()))
        self.chart.resize(event.size())
        super().resizeEvent(event)

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        self.callout.settext(f'X: {event.position().x():.2f} \nY: {event.position().y():.2f} ')
        self.callout.setPos(event.position())

        super().mouseMoveEvent(event)


app = QApplication([__file__])
v = View()
v.show()
raise SystemExit(app.exec())
