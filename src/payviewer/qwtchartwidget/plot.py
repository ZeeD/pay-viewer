from datetime import date
from datetime import timedelta
from itertools import cycle
from os import environ
from typing import TYPE_CHECKING

from guilib.chartslider.chartslider import date2days
from guilib.chartslider.chartslider import days2date

from payviewer.modelgui import SeriesModelFactory
from payviewer.modelgui import SeriesModelUnit
from qwt import QwtPlotCurve
from qwt import QwtPlotGrid
from qwt.plot import QwtPlot
from qwt.scale_div import QwtScaleDiv
from qwt.scale_draw import QwtScaleDraw

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCore import Qt
from qtpy.QtCore import Slot

if TYPE_CHECKING:
    from collections.abc import Iterable

    from qtpy.QtWidgets import QWidget

    from payviewer.viewmodel import SortFilterViewModel


def linecolors() -> 'Iterable[Qt.GlobalColor]':
    excluded: set[Qt.GlobalColor] = {
        Qt.GlobalColor.color0,
        Qt.GlobalColor.color1,
        Qt.GlobalColor.black,
        Qt.GlobalColor.white,
        Qt.GlobalColor.lightGray,
        Qt.GlobalColor.cyan,
        Qt.GlobalColor.green,
        Qt.GlobalColor.magenta,
        Qt.GlobalColor.yellow,
        Qt.GlobalColor.transparent,
    }
    return cycle(filter(lambda c: c not in excluded, Qt.GlobalColor))


def days(min_xdata: float, max_xdata: float) -> list[float]:
    lower = days2date(min_xdata)
    upper = days2date(max_xdata)

    def it() -> 'Iterable[float]':
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

    def it() -> 'Iterable[float]':
        wy, wm = ly, lm
        while (wy, wm) <= (uy, um):
            yield date2days(date(wy, wm, 1))
            if wm < 12:  # noqa: PLR2004
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

    def it() -> 'Iterable[float]':
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
    def from_unit(cls, unit: SeriesModelUnit) -> 'FmtScaleDraw':
        return cls(
            {
                SeriesModelUnit.EURO: '€ {value:_.2f}',
                SeriesModelUnit.HOUR: '{value:_} hours',
                SeriesModelUnit.DAY: '{value:_} days',
            }[unit]
        )


class YearMonthScaleDraw(QwtScaleDraw):
    def label(self, value: float) -> str:
        return days2date(value).strftime('%Y-%m')


class NoXDataError(Exception):
    def __init__(self) -> None:
        super().__init__('no *_xdata!')


class Plot(QwtPlot):
    def __init__(
        self,
        model: 'SortFilterViewModel',
        parent: 'QWidget | None',
        factory: SeriesModelFactory,
    ) -> None:
        super().__init__(parent)
        self.factory = factory
        self._model = model.sourceModel()

        self.setCanvasBackground(Qt.GlobalColor.white)
        QwtPlotGrid.make(self, enableminor=(False, True))
        self.setAxisScaleDraw(QwtPlot.xBottom, YearMonthScaleDraw())

        self._model.modelReset.connect(self.model_reset)

    @Slot()
    def model_reset(self) -> None:
        series_model = self.factory(self._model._infos)  # noqa: SLF001

        self.setAxisScaleDraw(
            QwtPlot.yLeft, FmtScaleDraw.from_unit(series_model.unit)
        )

        min_xdata: float | None = None
        max_xdata: float | None = None
        for serie, linecolor in zip(
            series_model.series, linecolors(), strict=False
        ):
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

            QwtPlotCurve.make(
                xdata,
                ydata,
                serie.name(),
                self,
                linecolor=linecolor,
                linewidth=2,
                antialiased=True,
            )

        if min_xdata is None or max_xdata is None:
            raise NoXDataError

        self.setAxisScaleDiv(QwtPlot.xBottom, QwtScaleDiv(
            min_xdata,
            max_xdata,
            days(min_xdata, max_xdata),
            months(min_xdata, max_xdata),
            years(min_xdata, max_xdata),
        ))

        self.replot()

    @Slot(date)
    def start_date_changed(self, start_date: date) -> None:
        lower_bound = date2days(start_date)

        interval = self.axisScaleDiv(QwtPlot.xBottom).interval()
        self.setAxisScaleDiv(QwtPlot.xBottom, QwtScaleDiv(
            lower_bound,
            interval.maxValue(),
            days(lower_bound, interval.maxValue()),
            months(lower_bound, interval.maxValue()),
            years(lower_bound, interval.maxValue()),
        ))

        self.replot()

    @Slot(date)
    def end_date_changed(self, end_date: date) -> None:
        upper_bound = date2days(end_date)

        interval = self.axisScaleDiv(QwtPlot.xBottom).interval()
        self.setAxisScaleDiv(QwtPlot.xBottom, QwtScaleDiv(
            interval.minValue(),
            upper_bound,
            days(interval.minValue(), upper_bound),
            months(interval.minValue(), upper_bound),
            years(interval.minValue(), upper_bound),
        ))

        self.replot()
