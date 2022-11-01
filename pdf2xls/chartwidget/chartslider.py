from datetime import date
from typing import Optional, cast

from PySide6.QtCore import Qt
from PySide6.QtCore import QUrl
from PySide6.QtCore import Signal
from PySide6.QtCore import Slot
from PySide6.QtQuick import QQuickItem
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget

from ..constants import CHARTSLIDER_QML_PATH
from ..viewmodel import SortFilterViewModel
from .common import date2days
from .common import days2date
from abc import abstractmethod


class RangeSlider(QQuickItem):
    first_moved: Signal
    second_moved: Signal

    @abstractmethod
    def set_first_value(self, first_value: float) -> None: ...

    @abstractmethod
    def set_second_value(self, second_value: float) -> None: ...


class ChartSlider(QWidget):
    start_date_changed = Signal(date)
    end_date_changed = Signal(date)

    def dump(self, status: QQuickView.Status) -> None:
        if status is QQuickView.Status.Error:
            for error in self.view.errors():
                print(f'{error=}')

    def __init__(self,
                 model: SortFilterViewModel,
                 parent: Optional[QWidget] = None):
        super().__init__(parent)
        layout = QVBoxLayout()
        self.setLayout(layout)
        self.view = QQuickView()
        self.view.statusChanged.connect(self.dump)
        self.view.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
        self.view.setSource(QUrl.fromLocalFile(CHARTSLIDER_QML_PATH))

        self.range_slider = cast(RangeSlider, self.view.rootObject())

        container = QWidget.createWindowContainer(self.view)
        container.setMinimumSize(100, 10)
        layout.addWidget(container)

        self._model = model
        self._model.sourceModel().modelReset.connect(self.source_model_reset)

        def _start_date_changed(days: int) -> None:
            self.start_date_changed.emit(days2date(days))
        self.range_slider.first_moved.connect(_start_date_changed)

        def _end_date_changed(days: int) -> None:
            self.end_date_changed.emit(days2date(days))
        self.range_slider.second_moved.connect(_end_date_changed)

    @Slot()
    def source_model_reset(self) -> None:
        source_model = self._model.sourceModel()
        dates: list[date] = [source_model.data(source_model.createIndex(row, 0),
                                               Qt.ItemDataRole.UserRole)
                             for row in range(0, source_model.rowCount())]
        dates.sort()
        minimum = date2days(dates[0])
        maximum = date2days(dates[-1])

        self.range_slider.setProperty('from', minimum)
        self.range_slider.setProperty('to', maximum)
        self.range_slider.set_first_value(minimum)
        self.range_slider.set_second_value(maximum)
