from abc import abstractmethod
from datetime import date
from logging import error
from typing import cast

from qtpy.QtCore import Qt
from qtpy.QtCore import QUrl
from qtpy.QtCore import Signal
from qtpy.QtCore import Slot
from qtpy.QtQuick import QQuickItem
from qtpy.QtQuick import QQuickView
from qtpy.QtWidgets import QVBoxLayout
from qtpy.QtWidgets import QWidget

from payviewer.constants import CHARTSLIDER_QML_PATH
from payviewer.dates import date2days
from payviewer.dates import days2date
from payviewer.viewmodel import SortFilterViewModel


class RangeSlider(QQuickItem):
    first_moved: Signal
    second_moved: Signal

    @abstractmethod
    def set_first_value(
        self,
        first_value: float,  # @UnusedVariable
    ) -> None:
        ...

    @abstractmethod
    def set_second_value(
        self,
        second_value: float,  # @UnusedVariable
    ) -> None:
        ...


class ChartSlider(QWidget):
    start_date_changed = Signal(date)
    end_date_changed = Signal(date)

    def dump(self, status: QQuickView.Status) -> None:
        if status is QQuickView.Status.Error:
            for error_ in self.view.errors():
                error('error=%s', error_)

    def __init__(
        self, model: SortFilterViewModel, parent: QWidget | None = None
    ) -> None:
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
        dates: list[date] = [
            source_model.data(
                source_model.createIndex(row, 0), Qt.ItemDataRole.UserRole
            )
            for row in range(source_model.rowCount())
        ]
        if not dates:
            error('no dates!')
            return
        dates.sort()
        minimum = date2days(dates[0])
        maximum = date2days(dates[-1])

        self.range_slider.setProperty('from', minimum)
        self.range_slider.setProperty('to', maximum)
        self.range_slider.set_first_value(minimum)
        self.range_slider.set_second_value(maximum)
