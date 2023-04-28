from collections.abc import Iterable
from datetime import date
from datetime import datetime
from datetime import time
from datetime import timedelta
from decimal import Decimal
from itertools import accumulate
from itertools import cycle
from operator import attrgetter
from sys import argv

from qtpy.QtCore import Qt
from qtpy.QtWidgets import QApplication
from qwt import QwtPlot
from qwt import QwtPlotCurve
from qwt import QwtPlotGrid
from qwt.scale_div import QwtScaleDiv
from qwt.scale_draw import QwtScaleDraw

from pdf2xls.loader import load
from pdf2xls.model import ColumnHeader
from pdf2xls.model import Info


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
    lower = date.fromtimestamp(min_xdata)
    upper = date.fromtimestamp(max_xdata)

    def it() -> Iterable[float]:
        when = lower
        while when < upper:
            yield datetime.combine(when, time()).timestamp()
            when += timedelta(days=1)
    return list(it())


def months(min_xdata: float, max_xdata: float) -> list[float]:
    lower = date.fromtimestamp(min_xdata)
    upper = date.fromtimestamp(max_xdata)

    ly, lm = (lower.year, lower.month)
    uy, um = (upper.year, upper.month)

    def it() -> Iterable[float]:
        wy, wm = ly, lm
        while (wy, wm) < (uy, um):
            yield datetime.combine(date(wy, wm, 1), time()).timestamp()
            if wm < 12:
                wm += 1
            else:
                wy += 1
                wm = 1
    return list(it())


def years(min_xdata: float, max_xdata: float) -> list[float]:
    lower = date.fromtimestamp(min_xdata).year
    upper = date.fromtimestamp(max_xdata).year

    def it() -> Iterable[float]:
        when = lower
        while when < upper:
            yield datetime.combine(date(when, 1, 1), time()).timestamp()
            when += 1
    return list(it())


class SD(QwtScaleDraw):
    def label(self, value: float) -> str:
        return date.fromtimestamp(value).strftime('%Y-%m')


def qwtmain(infos: list[Info]) -> QwtPlot:
    plot = QwtPlot()

    min_xdata: float | None = None
    max_xdata: float | None = None
    for (header, linecolor) in zip([ColumnHeader.netto_da_pagare], linecolors()):
        xdata: list[float] = []
        ydata: list[float] = []
        for when, howmuch in ((info.when, info.howmuch(header) or Decimal(0))
                              for info in infos):
            xdata.append(datetime.combine(when, time()).timestamp())
            ydata.append(float(howmuch))

        tmp = min(xdata)
        if min_xdata is None or tmp < min_xdata:
            min_xdata = tmp
        tmp = max(xdata)
        if max_xdata is None or tmp > max_xdata:
            max_xdata = tmp

        QwtPlotCurve.make(xdata, ydata, str(header), plot,
                          style=QwtPlotCurve.Steps,
                          linecolor=linecolor,
                          linewidth=3,
                          antialiased=True)

    if min_xdata is None or max_xdata is None:
        raise Exception('no *_xdata!')

    plot.setAxisScaleDiv(QwtPlot.xBottom,
                         QwtScaleDiv(min_xdata, max_xdata,
                                     days(min_xdata, max_xdata),
                                     months(min_xdata, max_xdata),
                                     years(min_xdata, max_xdata)))

    plot.setAxisScaleDraw(QwtPlot.xBottom, SD())

    QwtPlotGrid.make(plot)

    plot.resize(1_000, 1_000)
    return plot


PATH = '/home/zed/eclipse-workspace/pdf2xls-data'


def main() -> None:
    app = QApplication(argv)

    infos = load(PATH)
    plot = qwtmain(infos)
    plot.show()

    app.exec_()


if __name__ == '__main__':
    main()
