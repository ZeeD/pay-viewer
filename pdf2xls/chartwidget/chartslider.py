from datetime import date, timedelta
from typing import cast
from typing import Optional

from PySide6.QtCore import Qt, Signal
from PySide6.QtCore import Slot
from PySide6.QtWidgets import QSlider
from PySide6.QtWidgets import QWidget

from ..viewmodel import SortFilterViewModel


def date2days(d: date, *, epoch: date = date(1970, 1, 1)) -> int:
    return (d - epoch).days


def days2date(days: int, *, epoch: date = date(1970, 1, 1)) -> date:
    return epoch + timedelta(days=days)


class ChartSlider(QSlider):
    start_date_changed = Signal(date)

    def __init__(self,
                 model: SortFilterViewModel,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        self.model = model
        self.model.sourceModel().modelReset.connect(self.source_model_reset)
        self.setOrientation(Qt.Horizontal)
        self.setTickInterval(1)
        self.setTickPosition(QSlider.NoTicks)
        self.setSingleStep(1)

        def _start_date_changed(days: int) -> None:
            self.start_date_changed.emit(days2date(days))  # type: ignore
        self.valueChanged.connect(_start_date_changed)

    @Slot()
    def source_model_reset(self) -> None:
        source_model = self.model.sourceModel()
        dates: list[date] = [source_model.data(source_model.createIndex(row, 0),
                                               cast(int, Qt.UserRole))
                             for row in range(0, source_model.rowCount())]
        dates.sort()
        minimum = date2days(dates[0])
        maximum = date2days(dates[-1])

        self.setMinimum(minimum)
        self.setMaximum(maximum - 1)  # let at least 1 day of span
        self.setValue(minimum)
