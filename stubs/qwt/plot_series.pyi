from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt

class QwtPointArrayData:
    def xData(self) -> list[float]: ...
    def yData(self) -> list[float]: ...
    def sample(self, index: int) -> QPointF: ...

class QwtSeriesStore:
    def data(self) -> QwtPointArrayData | None: ...
    def setData(self, series: QwtPointArrayData | None) -> None: ...

class QwtPlotSeriesItem:
    def orientation(self) -> Qt.Orientation: ...