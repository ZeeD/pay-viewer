from typing import Optional

from PySide6.QtCore import Slot
from PySide6.QtWidgets import QSlider
from PySide6.QtWidgets import QWidget

from ..viewmodel import SortFilterViewModel


class ChartSlider(QSlider):
    def __init__(self,
                 model: SortFilterViewModel,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.model = model
        self.model.sourceModel().modelReset.connect(self.source_model_reset)
        self.setup_ui()

    def setup_ui(self) -> None:
        ...

    @Slot()
    def source_model_reset(self) -> None:
        ...
