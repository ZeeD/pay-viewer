from datetime import date
from typing import Optional, cast

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
        self.setChart(Chart(model))

    @Slot(date)
    def start_date_changed(self, start_date: date) -> None:
        cast(Chart, self.chart()).start_date_changed(start_date)
