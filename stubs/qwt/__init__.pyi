from PySide6.QtCore import Qt

from .plot import QwtPlot

class QwtPlotCurve:
    Steps: int

    @classmethod
    def make(  # noqa: PLR0913
        cls,
        xdata: list[float] | None = None,
        ydata: list[float] | None = None,
        title: str | None = None,
        plot: QwtPlot | None = None,
        z: None = None,
        x_axis: None = None,
        y_axis: None = None,
        style: int | None = None,
        symbol: None = None,
        linecolor: Qt.GlobalColor | None = None,
        linewidth: float | None = None,
        linestyle: None = None,
        antialiased: bool = False,  # noqa: FBT001,FBT002
        size: None = None,
        finite: None = None,
    ) -> QwtPlotCurve: ...

class QwtPlotGrid:
    @classmethod
    def make(  # noqa: PLR0913
        cls,
        plot: QwtPlot | None = None,
        z: None = None,
        enablemajor: tuple[bool, bool] | None = None,
        enableminor: tuple[bool, bool] | None = None,
        color: None = None,
        width: None = None,
        style: None = None,
        mincolor: None = None,
        minwidth: None = None,
        minstyle: None = None,
    ) -> QwtPlotGrid: ...
