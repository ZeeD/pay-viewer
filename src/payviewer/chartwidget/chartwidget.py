from typing import TYPE_CHECKING

from guilib.chartslider.chartslider import ChartSlider
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from payviewer.chartwidget.chartview import ChartView

if TYPE_CHECKING:
    from payviewer.modelgui import SeriesModelFactory
    from payviewer.viewmodel import SortFilterViewModel


class ChartWidget(QWidget):
    """Composition of a ChartView and a slider."""

    def __init__(
        self,
        model: 'SortFilterViewModel',
        parent: QWidget | None,
        factory: 'SeriesModelFactory',
    ) -> None:
        super().__init__(parent)

        chart_view = ChartView(model, self, factory)
        chart_slider = ChartSlider(model, self)

        layout = QVBoxLayout(self)
        layout.addWidget(chart_view)
        layout.addWidget(chart_slider)
        self.setLayout(layout)

        chart_slider.start_date_changed.connect(chart_view.start_date_changed)
        chart_slider.end_date_changed.connect(chart_view.end_date_changed)
