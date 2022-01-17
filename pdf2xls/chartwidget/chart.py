from typing import Optional

from PySide6.QtCharts import QChart
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QWidget

from ..viewmodel import SortFilterViewModel


class Chart(QChart):
    def __init__(self,
                 model: SortFilterViewModel,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.model = model
        self.model.sourceModel().modelReset.connect(self.source_model_reset)
        self.init()

    def init(self) -> None:
        ...

    @Slot()
    def source_model_reset(self) -> None:
        ...
