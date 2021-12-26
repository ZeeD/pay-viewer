from datetime import date
from decimal import Decimal
from typing import cast
from typing import Optional
from typing import Union

from PySide6.QtCore import QAbstractTableModel, QItemSelectionModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QObject
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt
from PySide6.QtGui import QBrush
from PySide6.QtGui import QColor

from .automation import try_fetch_new_data
from .loader import load
from .model import ColumnHeader
from .model import Info
from .model import parse_infos
from .settings import Settings
from PySide6.QtWidgets import QStatusBar


def by_column(info: Info, i: int) -> Optional[Decimal]:
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

    def rowCount(self, _parent: QModelIndex = QModelIndex()) -> int:
        return len(self._data)

    def columnCount(self, _parent: QModelIndex = QModelIndex()) -> int:
        return len(self._headers)

    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role: int = cast(int, Qt.DisplayRole)) -> Optional[str]:
        if role != cast(int, Qt.DisplayRole):
            return None

        if orientation != Qt.Horizontal:
            return None

        return self._headers[section]

    def data(self,
             index: QModelIndex,
             role: int = cast(int, Qt.DisplayRole)
             ) -> Union[str, Qt.Alignment, None, date, Decimal]:
        column = index.column()
        row = index.row()

        if role == cast(int, Qt.DisplayRole):
            return self._data[row][column]

        if role == cast(int, Qt.DecorationRole):
            return None

        if role == cast(int, Qt.ToolTipRole):
            return self._data[row][column]

        if role == cast(int, Qt.StatusTipRole):
            return None

        if role == cast(int, Qt.FontRole):
            return None

        if role == cast(int, Qt.TextAlignmentRole):
            return cast(Qt.Alignment, Qt.AlignCenter)

        if role == cast(int, Qt.BackgroundRole):
            max_, min_, this = max_min_this(self._data, row, column)
            perc = float((this - min_) / (max_ - min_)) if max_ != min_ else .5

            red = int((1 - perc) * 255)  # 0..1 ->  255..0
            green = int(perc * 255)  # 0..1 -> 0..255
            blue = int((.5 - abs(perc - .5)) * 511)  # 0..0.5..1 -> 0..255..0

            return QBrush(QColor(red, green, blue, 127))

            return None

        if role == cast(int, Qt.ForegroundRole):
            return None

        if role == cast(int, Qt.CheckStateRole):
            return None

        if role == cast(int, Qt.SizeHintRole):
            return None

        if role == cast(int, Qt.UserRole):
            # TODO: avoid losing types
            value = self._data[row][column]
            if column == 0:
                return value
            else:
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
             order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        def key(row: list[str]) -> Union[date, Decimal]:
            raw = row[index]
            return date.fromisoformat(raw) if index == 0 else Decimal(raw)

        self.layoutAboutToBeChanged.emit()
        try:
            self._data.sort(key=key, reverse=order == Qt.DescendingOrder)
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
        self.setFilterCaseSensitivity(Qt.CaseInsensitive)
        self.setSortCaseSensitivity(Qt.CaseInsensitive)
        self.setDynamicSortFilter(True)

    def filterAcceptsRow(self,
                         source_row: int,
                         source_parent: QModelIndex) -> bool:
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
        options = cast(QRegularExpression.PatternOptions,
                       QRegularExpression.CaseInsensitiveOption)
        self.setFilterRegularExpression(QRegularExpression(text, options))

    def sort(self,
             column: int,
             order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        self.sourceModel().sort(column, order)

    def selectionChanged(self,
                         selection_model: QItemSelectionModel,
                         statusbar: QStatusBar) -> None:
        bigsum = ''
        for index in cast(list[QModelIndex], selection_model.selectedRows(0)):
            data = index.data(cast(int, Qt.UserRole))
            bigsum = data

        statusbar.showMessage(f'⅀ = {bigsum}')

    def update(self, *, only_local: bool, force_pdf: bool) -> None:
        data_path = self.settings.data_path

        if not only_local:
            try_fetch_new_data(self.settings.username, self.settings.password,
                               data_path)

        self.sourceModel().load(load(data_path, force=force_pdf))
