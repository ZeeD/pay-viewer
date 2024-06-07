from PySide6.QtCore import Qt
from PySide6.QtWidgets import QFrame

from qwt.scale_div import QwtScaleDiv
from qwt.scale_draw import QwtScaleDraw

class QwtPlot(QFrame):
    xBottom: int  # noqa: N815
    yLeft: int  # noqa: N815

    def setAxisScaleDiv(self, axisId: int, scaleDiv: QwtScaleDiv) -> None: ...  # noqa: N802,N803
    def setAxisScaleDraw(  # noqa: N802
        self,
        axisId: int,  # noqa: N803
        scaleDraw: QwtScaleDraw,  # noqa: N803
    ) -> None: ...
    def axisScaleDiv(self, axisId: int) -> QwtScaleDiv: ...  # noqa: N802,N803
    def axisScaleDraw(self, axisId: int) -> QwtScaleDraw: ...  # noqa: N802,N803
    def replot(self) -> None: ...
    def setCanvasBackground(self, brush: Qt.GlobalColor) -> None: ...  # noqa: N802
    def setAxisScale(  # noqa: N802
        self,
        axisId: int,  # noqa: N803
        min_: float,
        max_: float,
        stepSize: float = 0,  # noqa: N803
    ) -> None: ...
