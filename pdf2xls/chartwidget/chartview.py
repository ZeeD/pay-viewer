from typing import Optional

from PySide6.QtCharts import QChartView
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from ..viewmodel import SortFilterViewModel
from .chart import Chart


class ChartView(QChartView):
    def __init__(self,
                 model: SortFilterViewModel,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.model = model
        self.model.sourceModel().modelReset.connect(self.source_model_reset)
        self.setup_ui()

    def setup_ui(self) -> None:
        chart = Chart(self.model)
        self.setChart(chart)

    @Slot()
    def source_model_reset(self) -> None:
        ...
