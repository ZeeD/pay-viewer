from typing import TYPE_CHECKING

from guilib.chartslider.xchartslider import XChartSlider
from guilib.chartslider.ychartslider import YChartSlider
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QWidget

from payviewer.qwtchartwidget.plot import Plot

if TYPE_CHECKING:
    from payviewer.modelgui import SeriesModelFactory
    from payviewer.viewmodel import SortFilterViewModel


class QwtChartVidget(QWidget):
    """Composition of a Plot and a slider."""

    def __init__(
        self,
        model: 'SortFilterViewModel',
        parent: QWidget | None,
        factory: 'SeriesModelFactory',
    ) -> None:
        super().__init__(parent)

        plot = Plot(model, self, factory)
        x_chart_slider = XChartSlider(model, self, dates_column=0)
        y_chart_slider = YChartSlider(model, self, dates_column=0)

        layout = QGridLayout(self)
        layout.addWidget(plot, 0, 0)
        layout.addWidget(x_chart_slider, 1, 0)
        layout.addWidget(y_chart_slider, 0, 1)
        self.setLayout(layout)

        x_chart_slider.start_date_changed.connect(plot.start_date_changed)
        x_chart_slider.end_date_changed.connect(plot.end_date_changed)

        y_chart_slider.min_money_changed.connect(plot.min_money_changed)
        y_chart_slider.max_money_changed.connect(plot.max_money_changed)
