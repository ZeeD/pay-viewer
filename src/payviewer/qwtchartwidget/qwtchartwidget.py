from typing import TYPE_CHECKING

from guilib.chartslider.chartslider import ChartSlider
from PySide6.QtWidgets import QVBoxLayout
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
        chart_slider = ChartSlider(model, self, dates_column=1)

        layout = QVBoxLayout(self)
        layout.addWidget(plot)
        layout.addWidget(chart_slider)
        self.setLayout(layout)

        chart_slider.start_date_changed.connect(plot.start_date_changed)
        chart_slider.end_date_changed.connect(plot.end_date_changed)
