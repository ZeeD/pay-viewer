from datetime import date
from decimal import Decimal
from typing import cast
from typing import Literal
from typing import overload

from qtpy.QtCore import QAbstractTableModel
from qtpy.QtCore import QItemSelectionModel
from qtpy.QtCore import QModelIndex
from qtpy.QtCore import QObject
from qtpy.QtCore import QPersistentModelIndex
from qtpy.QtCore import QRegularExpression
from qtpy.QtCore import QSortFilterProxyModel
from qtpy.QtCore import Qt
from qtpy.QtGui import QBrush
from qtpy.QtGui import QColor
from qtpy.QtWidgets import QStatusBar

from .automation import try_fetch_new_data
from .loader import load
from .model import ColumnHeader
from .model import Info
from .model import parse_infos
from .settings import Settings


def by_column(info: Info, i: int) -> Decimal | None:
    column_header = ColumnHeader(i)
    for column in info.columns:
        if column.header == column_header:
            return column.howmuch
    return None


def max_min_this(data: list[list[str]],
                 row: int, column: int) -> tuple[Decimal, Decimal, Decimal]:
    ds = [Decimal(date.fromisoformat(datum[0]).toordinal())
          for datum in data] if column == 0 else [Decimal(datum[column])
                                                  for datum in data]
    return max(ds), min(ds), ds[row]


class ViewModel(QAbstractTableModel):

    def __init__(self, parent: QObject, infos: list[Info]):
        super().__init__(parent)
        self._set_infos(infos)

    def _set_infos(self, infos: list[Info]) -> None:
        self._headers, self._data = parse_infos(infos)
        self._infos = infos

    def rowCount(self, _parent: QModelIndex | QPersistentModelIndex=QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, _parent: QModelIndex | QPersistentModelIndex=QModelIndex()) -> int:
        return len(self._headers)

    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role: int=Qt.ItemDataRole.DisplayRole) -> str | None:
        if role != Qt.ItemDataRole.DisplayRole:
            return None

        if orientation != Qt.Orientation.Horizontal:
            return None

        return self._headers[section]

    @overload
    def data(self,
             # white liar, we need also to add a rule on index --> col 0
             index: QModelIndex | QPersistentModelIndex,  # @UnusedVariable
             role: Literal[Qt.ItemDataRole.UserRole]  # @UnusedVariable
             ) -> date: ...

    @overload
    def data(self,
             index: QModelIndex | QPersistentModelIndex,  # @UnusedVariable
             role: int=Qt.ItemDataRole.DisplayRole  # @UnusedVariable
             ) -> str | Qt.AlignmentFlag | None | date | Decimal | QBrush: ...

    def data(self,
             index: QModelIndex | QPersistentModelIndex,
             role: int=Qt.ItemDataRole.DisplayRole
             ) -> str | Qt.AlignmentFlag | None | date | Decimal | QBrush:
        column = index.column()
        row = index.row()

        if role == Qt.ItemDataRole.DisplayRole:
            value = self._data[row][column]
            if column == 0:
                return value[:-3] if value.endswith('01') else f'{value[:-5]}13'
            if value == '0':
                return None
            return value

        if role == Qt.ItemDataRole.DecorationRole:
            return None

        if role == Qt.ItemDataRole.ToolTipRole:
            return self._data[row][column]

        if role == Qt.ItemDataRole.StatusTipRole:
            return None

        if role == Qt.ItemDataRole.FontRole:
            return None

        if role == Qt.ItemDataRole.TextAlignmentRole:
            return Qt.AlignmentFlag.AlignCenter

        if role == Qt.ItemDataRole.BackgroundRole:
            max_, min_, val = max_min_this(self._data, row, column)
            if val == 0:
                return None

            perc = (val - min_) / (max_ - min_) if max_ != min_ else Decimal(.5)

            hue = int(perc * 120)   # 0..359 ; red=0, green=120
            saturation = 223        # 0..255
            lightness = 159         # 0..255

            return QBrush(QColor.fromHsl(hue, saturation, lightness))


        if role == Qt.ItemDataRole.ForegroundRole:
            return None

        if role == Qt.ItemDataRole.CheckStateRole:
            return None

        if role == Qt.ItemDataRole.SizeHintRole:
            return None

        if role == Qt.ItemDataRole.UserRole:
            # TODO: avoid losing types
            if column == 0:
                return self._infos[row].when
            else:
                value = self._data[row][column]
                return Decimal(value) if value is not None else None

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

        print(f'{role=!r}')
        return None

    def sort(self,
             index: int,
             order: Qt.SortOrder=Qt.SortOrder.AscendingOrder) -> None:

        def key(row: list[str]) -> date | Decimal:
            raw = row[index]
            return date.fromisoformat(raw) if index == 0 else Decimal(raw)

        self.layoutAboutToBeChanged.emit()
        try:
            self._data.sort(key=key,
                            reverse=order == Qt.SortOrder.AscendingOrder)
        finally:
            self.layoutChanged.emit()

    def load(self, infos: list[Info]) -> None:
        self.beginResetModel()
        try:
            self._set_infos(infos)
        finally:
            self.endResetModel()


class SortFilterViewModel(QSortFilterProxyModel):

    def __init__(self, settings: Settings) -> None:
        super().__init__()
        self.settings = settings
        self.setSourceModel(ViewModel(self, []))
        self.setFilterCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseSensitivity.CaseInsensitive)
        self.setDynamicSortFilter(True)

    def filterAcceptsRow(self,
                         source_row: int,
                         source_parent: QModelIndex | QPersistentModelIndex) -> bool:
        regex = self.filterRegularExpression()
        source_model = self.sourceModel()
        column_count = source_model.columnCount(source_parent)

        return any(regex.match(str(source_model.data(index))).hasMatch()
                   for index in (source_model.index(source_row,
                                                    i,
                                                    source_parent)
                                 for i in range(column_count)))

    def filterChanged(self, text: str) -> None:
        text = QRegularExpression.escape(text)
        options = QRegularExpression.PatternOption.CaseInsensitiveOption
        self.setFilterRegularExpression(QRegularExpression(text, options))

    def sort(self,
             column: int,
             order: Qt.SortOrder=Qt.SortOrder.AscendingOrder) -> None:
        self.sourceModel().sort(column, order)

    def selectionChanged(self,
                         selection_model: QItemSelectionModel,
                         statusbar: QStatusBar) -> None:
        column = selection_model.currentIndex().column()
        if column == 0:
            message = ''
        else:
            bigsum = sum(index.data(Qt.ItemDataRole.UserRole)
                         for index in selection_model.selectedRows(column))
            message = f'⅀ = {bigsum}'
        statusbar.showMessage(message)

    def update(self, *, only_local: bool, force_pdf: bool) -> None:
        data_path = self.settings.data_path

        if not only_local:
            try_fetch_new_data(self.settings.username, self.settings.password,
                               data_path)

        if data_path:
            self.sourceModel().load(load(data_path, force=force_pdf))

    def get_categories(self) -> list[str]:
        view_model = self.sourceModel()
        return view_model._headers

    def get_rows(self) -> list[Info]:
        view_model = self.sourceModel()
        return view_model._infos

    def sourceModel(self) -> ViewModel:
        return cast(ViewModel, super().sourceModel())
