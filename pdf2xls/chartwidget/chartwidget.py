from typing import Optional

from PySide6.QtCore import Slot
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
        self.model = model
        self.model.sourceModel().modelReset.connect(self.source_model_reset)
        self.setup_ui()

    def setup_ui(self) -> None:
        layout = QVBoxLayout(self)
        chart_view = ChartView(self.model, self)
        chart_slider = ChartSlider(self.model, self)
        layout.addWidget(chart_view)
        layout.addWidget(chart_slider)
        self.setLayout(layout)

    @Slot()
    def source_model_reset(self) -> None:
        ...
