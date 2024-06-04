from datetime import date
from datetime import timedelta

from guilib.chartslider.chartslider import date2days
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QSlider
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from qwt import QwtPlot
from qwt import QwtPlotGrid
from qwt.plot_curve import QwtPlotCurve
from qwt.scale_div import QwtScaleDiv
from qwt.scale_draw import QwtScaleDraw

EPOCH = date(1970, 1, 1)


def date2days(d: date, *, epoch: date = EPOCH) -> int:
    return (d - epoch).days


def days2date(days: float, *, epoch: date = EPOCH) -> date:
    return epoch + timedelta(days=days)


class EuroScaleDraw(QwtScaleDraw):
    def label(self, value: float) -> str:
        return f'€ {value:_.2f}'

class YearMonthScaleDraw(QwtScaleDraw):
    def label(self, value: float) -> str:
        return days2date(value).strftime('%Y-%m')

def change_start_date(days: int) -> None:
    scale_div = plot.axisScaleDiv(QwtPlot.xBottom)
    scale_div.setLowerBound(days)
    plot.replot()

# main

app = QApplication([__file__])

root = QWidget()

layout = QVBoxLayout(root)

plot = QwtPlot(root)
QwtPlotGrid.make(plot, enableminor=(False, True))
plot.setAxisScaleDraw(QwtPlot.xBottom, YearMonthScaleDraw())
plot.setAxisScaleDraw(QwtPlot.yLeft, EuroScaleDraw())
QwtPlotCurve.make(
    [date2days(day) for day in (
        date(2020,1,1),
        date(2021,1,1),
        date(2022,1,1),
        date(2022,2,1),
        date(2022,8,1),
        date(2024,1,1),
    )],
    [1,2,100,1000,300,33],
    '...',
    plot,
    linecolor=Qt.GlobalColor.red,
    antialiased=True,
)
plot.setAxisScaleDiv(QwtPlot.xBottom, QwtScaleDiv(
            date2days(date(2020,1,1)),
            date2days(date(2024,1,1)),
            [],
            [
                date2days(date(year,month,1)) for year in range(2020,2025)
             for month in range(1,13)
            ],
            [date2days(date(year,1,1)) for year in range(2020,2025)],
        ))


slider = QSlider(Qt.Orientation.Horizontal, root)
slider.setRange(date2days(date(2020,1,1)),
                date2days(date(2024,1,1))
                )

layout.addWidget(plot)
layout.addWidget(slider)

root.setLayout(layout)

slider.valueChanged.connect(change_start_date)

root.show()

raise SystemExit(app.exec())

