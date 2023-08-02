from __future__ import annotations

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
from ..modelgui import SeriesModelUnit
from ..viewmodel import SortFilterViewModel


def linecolors() -> Iterable[Qt.GlobalColor]:
    excluded: set[Qt.GlobalColor] = set([Qt.GlobalColor.color0,
                                         Qt.GlobalColor.color1,
                                         Qt.GlobalColor.black,
                                         Qt.GlobalColor.white,
                                         Qt.GlobalColor.lightGray,
                                         Qt.GlobalColor.cyan,
                                         Qt.GlobalColor.green,
                                         Qt.GlobalColor.magenta,
                                         Qt.GlobalColor.yellow,
                                         Qt.GlobalColor.transparent])
    return cycle(filter(lambda c: c not in excluded, Qt.GlobalColor))


def normalized_xdatas(min_xdata: float, max_xdata: float) -> tuple[float, float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    return (date2days(date(lower.year, 1, 1)),
            date2days(date(upper.year + 1, 1, 1)))


def days(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    def it() -> Iterable[float]:
        when = lower
        while when <= upper:
            yield date2days(when)
            when += timedelta(days=7)
    return list(it())


def months(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    ly, lm = (lower.year, lower.month)
    uy, um = (upper.year, upper.month)

    def it() -> Iterable[float]:
        wy, wm = ly, lm
        while (wy, wm) <= (uy, um):
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
        while wy <= uy:
            yield date2days(date(wy, 1, 1))
            wy += 1
    return list(it())


class FmtScaleDraw(QwtScaleDraw):
    def __init__(self, fmt: str) -> None:
        super().__init__()
        self.fmt = fmt

    def label(self, value: float) -> str:
        return self.fmt.format(value=value)

    @classmethod
    def from_unit(cls, unit: SeriesModelUnit) -> FmtScaleDraw:
        return cls({
            SeriesModelUnit.EURO: '€ {value:_.2f}',
            SeriesModelUnit.HOUR: '{value:_} hours',
            SeriesModelUnit.DAY: '{value:_} days',
        }[unit])


class YearMonthScaleDraw(QwtScaleDraw):
    def label(self, value: float) -> str:
        return days2date(value).strftime('%Y-%m')


class Plot(QwtPlot):
    def __init__(self,
                 model: SortFilterViewModel,
                 parent: QWidget | None,
                 factory: SeriesModelFactory):
        super().__init__(parent)
        self.factory = factory
        self._model = model.sourceModel()

        self.setCanvasBackground(Qt.GlobalColor.white)
        QwtPlotGrid.make(self,
                         enableminor=(False, True))
        self.setAxisScaleDraw(QwtPlot.xBottom, YearMonthScaleDraw())

        self._model.modelReset.connect(self.model_reset)

    @Slot()
    def model_reset(self) -> None:
        series_model = self.factory(self._model._infos)

        self.setAxisScaleDraw(QwtPlot.yLeft,
                              FmtScaleDraw.from_unit(series_model.unit))

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
                              # style=QwtPlotCurve.Dots,
                              # linewidth=5,
                              antialiased=True)

        if min_xdata is None or max_xdata is None:
            raise Exception('no *_xdata!')
        normalized_min_xdata, normalized_max_xdata = normalized_xdatas(min_xdata, max_xdata)

        x_scale_div = QwtScaleDiv(min_xdata, max_xdata,
                                  days(normalized_min_xdata, normalized_max_xdata),
                                  months(normalized_min_xdata, normalized_max_xdata),
                                  years(normalized_min_xdata, normalized_max_xdata))
        self.setAxisScaleDiv(QwtPlot.xBottom, x_scale_div)

        # self.setAxisScale(QwtPlot.xBottom, x_scale_div.lowerBound(), x_scale_div.upperBound())
        self.replot()

    @Slot(date)
    def start_date_changed(self, start_date: date) -> None:
        lower_bound = date2days(start_date)

        scale_div = self.axisScaleDiv(QwtPlot.xBottom)
        scale_div.setLowerBound(lower_bound)

        # scale_draw = self.axisScaleDraw(QwtPlot.xBottom)
        # pos = scale_draw.pos()
        # length = scale_draw.length()
        # print(f'{pos=}, {length=}')
        # scale_draw.move(pos.x()+1, 0)
        # scale_draw.setLength(length-1)

        # self.setAxisScale(QwtPlot.xBottom, scale_div.lowerBound(), scale_div.upperBound())
        self.replot()

    @Slot(date)
    def end_date_changed(self, end_date: date) -> None:
        upper_bound = date2days(end_date)

        scale_div = self.axisScaleDiv(QwtPlot.xBottom)
        scale_div.setUpperBound(upper_bound)

        # self.setAxisScale(QwtPlot.xBottom, scale_div.lowerBound(), scale_div.upperBound())
        self.replot()
