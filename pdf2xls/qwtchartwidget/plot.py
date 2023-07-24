from collections.abc import Iterable
from datetime import date
from datetime import timedelta
from itertools import cycle

from qtpy.QtCore import Qt
from qtpy.QtCore import Slot
from qtpy.QtWidgets import QWidget
from qwt import QwtPlot
from qwt import QwtPlotCurve
from qwt import QwtPlotGrid
from qwt.scale_div import QwtScaleDiv
from qwt.scale_draw import QwtScaleDraw

from ..dates import date2days
from ..dates import days2date
from ..modelgui import SeriesModelFactory
from ..viewmodel import SortFilterViewModel


def linecolors(excluded: set[Qt.GlobalColor]=set([Qt.GlobalColor.color0,
                                                  Qt.GlobalColor.color1,
                                                  Qt.GlobalColor.black,
                                                  Qt.GlobalColor.white,
                                                  Qt.GlobalColor.darkGray,
                                                  Qt.GlobalColor.gray,
                                                  Qt.GlobalColor.lightGray,
                                                  Qt.GlobalColor.transparent])) -> Iterable[Qt.GlobalColor]:
    return cycle(filter(lambda c: c not in excluded, Qt.GlobalColor))


def days(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    def it() -> Iterable[float]:
        when = lower
        while when < upper:
            yield date2days(when)
            when += timedelta(days=1)
    return list(it())


def months(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    ly, lm = (lower.year, lower.month)
    uy, um = (upper.year, upper.month)

    def it() -> Iterable[float]:
        wy, wm = ly, lm
        while (wy, wm) < (uy, um):
            yield date2days(date(wy, wm, 1))
            if wm < 12:
                wm += 1
            else:
                wy += 1
                wm = 1
    return list(it())


def years(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    ly = lower.year
    uy = upper.year

    def it() -> Iterable[float]:
        wy = ly
        while wy < uy:
            yield date2days(date(wy, 1, 1))
            wy += 1
    return list(it())


class SD(QwtScaleDraw):
    def label(self, value: float) -> str:
        return days2date(value).strftime('%Y-%m')


class Plot(QwtPlot):
    def __init__(self,
                 model: SortFilterViewModel,
                 parent: QWidget | None,
                 factory: SeriesModelFactory):
        super().__init__(parent)
        self._model = model.sourceModel()
        self._model.modelReset.connect(self.model_reset)
        self.factory = factory

    @Slot()
    def model_reset(self) -> None:
        series_model = self.factory(self._model._infos)

        min_xdata: float | None = None
        max_xdata: float | None = None
        for (serie, linecolor) in zip(series_model.series, linecolors()):
            xdata: list[float] = []
            ydata: list[float] = []
            for point in serie.points():
                when, howmuch = point.x(), point.y()
                xdata.append(when)
                ydata.append(howmuch)

            tmp = min(xdata)
            if min_xdata is None or tmp < min_xdata:
                min_xdata = tmp
            tmp = max(xdata)
            if max_xdata is None or tmp > max_xdata:
                max_xdata = tmp

            QwtPlotCurve.make(xdata, ydata, serie.name(), self,
                              linecolor=linecolor,
                              linewidth=3,
                              antialiased=True)

        if min_xdata is None or max_xdata is None:
            raise Exception('no *_xdata!')

        self.setAxisScaleDiv(QwtPlot.xBottom,
                             QwtScaleDiv(min_xdata, max_xdata,
                                         days(min_xdata, max_xdata),
                                         months(min_xdata, max_xdata),
                                         years(min_xdata, max_xdata)))

        self.setAxisScaleDraw(QwtPlot.xBottom, SD())

        QwtPlotGrid.make(self)
