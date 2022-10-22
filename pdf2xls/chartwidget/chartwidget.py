from typing import Optional

from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from ..viewmodel import SortFilterViewModel
from .chartslider import ChartSlider
from .chartview import ChartView


class ChartWidget(QWidget):
    'composition of a ChartView and a slider'

    def __init__(self,
                 model: SortFilterViewModel,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)

        layout = QVBoxLayout(self)
        chart_view = ChartView(model, self)
        chart_slider = ChartSlider(model, self)
        layout.addWidget(chart_view)
        layout.addWidget(chart_slider)
        self.setLayout(layout)

        chart_slider.start_date_changed.connect(chart_view.start_date_changed)
        chart_slider.end_date_changed.connect(chart_view.end_date_changed)
