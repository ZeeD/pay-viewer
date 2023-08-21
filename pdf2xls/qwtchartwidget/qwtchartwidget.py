from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

from ..chartslider.chartslider import ChartSlider
from ..modelgui import SeriesModelFactory
from ..viewmodel import SortFilterViewModel
from .plot import Plot


class QwtChartVidget(QWidget):
    'composition of a ChartView and a slider'

    def __init__(self,
                 model: SortFilterViewModel,
                 parent: QWidget | None,
                 factory: SeriesModelFactory):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        plot = Plot(model, self, factory)
        chart_slider = ChartSlider(model, self)
        layout.addWidget(plot)
        layout.addWidget(chart_slider)
        self.setLayout(layout)

        chart_slider.start_date_changed.connect(plot.start_date_changed)
        chart_slider.end_date_changed.connect(plot.end_date_changed)
