from datetime import date
from decimal import Decimal
from pathlib import Path
from typing import TYPE_CHECKING
from typing import Literal
from typing import cast
from typing import overload
from typing import override

from guilib.searchsheet.model import SearchableModel
from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QObject
from PySide6.QtCore import QPersistentModelIndex
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor
from PySide6.QtGui import QIcon

from payviewer.automation import try_fetch_new_data
from payviewer.loader import load
from payviewer.model import ZERO
from payviewer.model import ColumnHeader
from payviewer.model import Info
from payviewer.model import parse_infos

if TYPE_CHECKING:
    from PySide6.QtWidgets import QStatusBar

    from payviewer.settings import Settings


def by_column(info: Info, i: int) -> Decimal | None:
    column_header = ColumnHeader(i)
    for column in info.columns:
        if column.header == column_header:
            return column.howmuch
    return None


def max_min_whens(
    whens: list[tuple[Path, date]], row: int
) -> tuple[Decimal, Decimal, Decimal]:
    ds = [Decimal(when.toordinal()) for _, when in whens]
    return max(ds), min(ds), ds[row]


def max_min_this(
    data: list[list[Decimal]], row: int, column: int
) -> tuple[Decimal, Decimal, Decimal]:
    ds = [datum[column] for datum in data]
    return max(ds), min(ds), ds[row]


_QMODELINDEX = QModelIndex()

PATH_ROLE = Qt.ItemDataRole.UserRole + 1


class ViewModel(QAbstractTableModel):
    def __init__(self, parent: QObject | None, infos: list[Info]) -> None:
        super().__init__(parent)
        self._set_infos(infos)

    def _set_infos(self, infos: list[Info]) -> None:
        self._headers, self._whens, self._data = parse_infos(infos)
        self._infos = infos

    @override
    def rowCount(
        self, _parent: QModelIndex | QPersistentModelIndex = _QMODELINDEX
    ) -> int:
        return len(self._data)

    @override
    def columnCount(
        self, _parent: QModelIndex | QPersistentModelIndex = _QMODELINDEX
    ) -> int:
        return len(self._headers)

    @override
    def headerData(
        self,
        section: int,
        orientation: Qt.Orientation,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> str | None:
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation != Qt.Orientation.Horizontal:
            return None

        return self._headers[section]

    @overload
    def data(
        self,
        # white liar, we need also to add a rule on index --> col 0
        index: QModelIndex | QPersistentModelIndex,  # @UnusedVariable
        role: Literal[Qt.ItemDataRole.UserRole],  # @UnusedVariable
    ) -> date: ...

    @overload
    def data(
        self,
        index: QModelIndex | QPersistentModelIndex,  # @UnusedVariable
        role: int = Qt.ItemDataRole.DisplayRole,  # @UnusedVariable
    ) -> (
        'str | Qt.AlignmentFlag | None | date | Decimal | QBrush | QIcon | Path'
    ): ...

    @override
    def data(  # noqa: PLR0911
        self,
        index: QModelIndex | QPersistentModelIndex,
        role: int = Qt.ItemDataRole.DisplayRole,
    ) -> (
        'str | Qt.AlignmentFlag | None | date | Decimal | QBrush | QIcon | Path'
    ):
        column = index.column()
        row = index.row()

        if role == Qt.ItemDataRole.DecorationRole:
            if column == 0:
                return QIcon.fromTheme(QIcon.ThemeIcon.DocumentPrintPreview)
            return None

        if role in {Qt.ItemDataRole.DisplayRole, Qt.ItemDataRole.ToolTipRole}:
            if column == 0:
                when = self._whens[row][1]
                return f'{when}' if when.day == 1 else f'{when:%Y-%m}-13'
            value = self._data[row][column - 1]
            return None if value == ZERO else str(value)

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.BackgroundRole:
            if column == 0:
                max_, min_, val = max_min_whens(self._whens, row)
            else:
                max_, min_, val = max_min_this(self._data, row, column - 1)
            if val == 0:
                return None

            perc = (
                (val - min_) / (max_ - min_) if max_ != min_ else Decimal(0.5)
            )

            hue = int(perc * 120)  # 0..359 ; red=0, green=120
            saturation = 223  # 0..255
            lightness = 159  # 0..255

            return QBrush(QColor.fromHsl(hue, saturation, lightness))

        if role == Qt.ItemDataRole.UserRole:
            if column == 0:
                return self._whens[row][1]

            return self._data[row][column - 1]

        if role == PATH_ROLE:
            if column == 0:
                return self._whens[row][0]
            raise ValueError

        # DisplayRole 0
        # DecorationRole 1
        # EditRole 2
        # ToolTipRole 3
        # StatusTipRole 4
        # WhatsThisRole 5
        # FontRole 6
        # TextAlignmentRole 7
        # BackgroundRole 8
        # ForegroundRole 9
        # CheckStateRole 10
        # AccessibleTextRole 11
        # AccessibleDescriptionRole 12
        # SizeHintRole 13
        # InitialSortOrderRole 14
        # DisplayPropertyRole 27
        # DecorationPropertyRole 28
        # ToolTipPropertyRole 29
        # StatusTipPropertyRole 30
        # WhatsThisPropertyRole 31
        # UserRole 256
        return None

    @override
    def sort(
        self, index: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder
    ) -> None:
        idxs = list(range(len(self._whens)))
        key = (
            self._whens.__getitem__
            if index == 0
            else lambda i: self._data[i][index - 1]
        )
        idxs.sort(key=key, reverse=order == Qt.SortOrder.AscendingOrder)

        self.layoutAboutToBeChanged.emit()
        try:
            self._whens[:] = map(self._whens.__getitem__, idxs)
            self._data[:] = map(self._data.__getitem__, idxs)
        finally:
            self.layoutChanged.emit()

    def load(self, infos: list[Info]) -> None:
        self.beginResetModel()
        try:
            self._set_infos(infos)
        finally:
            self.endResetModel()


class SortFilterViewModel(SearchableModel):
    def __init__(
        self, settings: 'Settings', parent: QObject | None = None
    ) -> None:
        super().__init__(ViewModel(parent, []), parent)
        self.settings = settings

    @override
    def sourceModel(self) -> ViewModel:
        return cast(ViewModel, super().sourceModel())

    def sort(
        self, column: int, order: Qt.SortOrder = Qt.SortOrder.AscendingOrder
    ) -> None:
        self.sourceModel().sort(column, order)

    def selection_changed(
        self, selection_model: QItemSelectionModel, statusbar: 'QStatusBar'
    ) -> None:
        column = selection_model.currentIndex().column()
        if column == 0:
            message = ''
        else:
            bigsum = sum(
                index.data(Qt.ItemDataRole.UserRole)
                for index in selection_model.selectedRows(column)
            )
            message = f'⅀ = {bigsum}'
        statusbar.showMessage(message)

    def update(self, *, only_local: bool, force_pdf: bool) -> None:
        data_path = self.settings.data_path

        if not only_local:
            try_fetch_new_data(
                self.settings.username, self.settings.password, data_path
            )

        if data_path:
            self.sourceModel().load(load(data_path, force=force_pdf))

    def get_categories(self) -> list[str]:
        view_model = self.sourceModel()
        return view_model._headers  # noqa: SLF001

    def get_rows(self) -> list[Info]:
        view_model = self.sourceModel()
        return view_model._infos  # noqa: SLF001
