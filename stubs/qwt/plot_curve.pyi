from PySide6.QtCore import QPoint
from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt
from PySide6.QtGui import QPen

from qwt.plot import QwtPlot
from qwt.plot_series import QwtSeriesStore
from qwt.text import QwtText

class QwtPlotCurve(QwtSeriesStore):
    Steps: int

    @classmethod
    def make(
        cls,
        xdata: list[float] | None = None,
        ydata: list[float] | None = None,
        title: str | QwtText | None = None,
        plot: QwtPlot | None = None,
        z: None = None,
        x_axis: None = None,
        y_axis: None = None,
        style: int | None = None,
        symbol: None = None,
        linecolor: Qt.GlobalColor | None = None,
        linewidth: float | None = None,
        linestyle: None = None,
        antialiased: bool = False,
        size: None = None,
        finite: None = None,
    ) -> QwtPlotCurve: ...
    def closestPoint(self, pos: QPointF | QPoint) -> tuple[int, float]: ...
    def pen(self) -> QPen: ...
