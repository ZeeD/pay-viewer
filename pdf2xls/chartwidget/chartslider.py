from datetime import date, timedelta
from typing import cast
from typing import Optional

from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QSlider
from PySide6.QtWidgets import QWidget

from ..viewmodel import SortFilterViewModel


def d2days(d: date, *, epoch: date = date(1970, 1, 1)) -> int:
    return (d - epoch).days


def days2d(days: int, *, epoch: date = date(1970, 1, 1)) -> date:
    return epoch + timedelta(days=days)


class ChartSlider(QSlider):
    def __init__(self,
                 model: SortFilterViewModel,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.model = model
        self.model.sourceModel().modelReset.connect(self.source_model_reset)
        self.init()

    def init(self) -> None:
        self.setOrientation(Qt.Horizontal)
        self.setTickInterval(0)
        self.setTickPosition(QSlider.TicksBelow)
        self.valueChanged.connect(lambda days: print(f'{days2d(days)=}'))

    @Slot()
    def source_model_reset(self) -> None:
        source_model = self.model.sourceModel()
        dates: list[date] = [source_model.data(source_model.createIndex(row, 0),
                                               cast(int, Qt.UserRole))
                             for row in range(0, source_model.rowCount())]
        dates.sort()
        minimum = d2days(dates[0])
        maximum = d2days(dates[-1])

        self.setMinimum(minimum)
        self.setMaximum(maximum)
        self.setValue(maximum)
