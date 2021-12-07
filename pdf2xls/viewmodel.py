from datetime import date
from decimal import Decimal
from typing import List
from typing import Optional
from typing import Union
from typing import cast

from PySide6.QtCore import QAbstractTableModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import QObject
from PySide6.QtCore import QRegularExpression
from PySide6.QtCore import QSortFilterProxyModel
from PySide6.QtCore import Qt

from .model import ColumnHeader
from .model import Info


def by_column(info: Info, i: int) -> Optional[Decimal]:
    column_header = ColumnHeader(i)
    for column in info.columns:
        if column.header == column_header:
            return column.howmuch
    return None


class ViewModel(QAbstractTableModel):
    def __init__(self, parent: QObject, infos: List[Info]):
        super().__init__(parent)
        self._set_infos(infos)

    def _set_infos(self, infos: List[Info]) -> None:
        self._infos = infos

    def rowCount(self, _parent: QModelIndex = QModelIndex()) -> int:
        return len(self._infos)

    def columnCount(self, _parent: QModelIndex = QModelIndex()) -> int:
        return 1 + len(ColumnHeader) - 1 + max(len(info.additional_details)
                                               for info in self._infos)

    def headerData(self,
                   section: int,
                   orientation: Qt.Orientation,
                   role: int = cast(int, Qt.DisplayRole)) -> Optional[str]:
        if role != cast(int, Qt.DisplayRole):
            return None

        if orientation != Qt.Horizontal:
            return None

        if section == 0:
            return 'month'
        if section < 1 + len(ColumnHeader):
            return ColumnHeader(section).name
        return f'TODO {section}'

    def data(self,
             index: QModelIndex,
             role: int = cast(int, Qt.DisplayRole)
             ) -> Optional[Union[str, date, Decimal]]:
        column = index.column()
        row = index.row()

        if role == cast(int, Qt.DisplayRole):
            if column == 0:
                return str(self._infos[row].when)
            if column < 1 + len(ColumnHeader):
                ret = str(by_column(self._infos[row], column))
                return ret
            return f'TODO {row}x{column}'

        # if role == Qt.BackgroundRole:
        #     abs_value = _abs(self._data[row])
        #     perc = float((abs_value - self._min) / (self._max - self._min))
        #
        #     red = int((1 - perc) * 255)  # 0..1 ->  255..0
        #     green = int(perc * 255)  # 0..1 -> 0..255
        #     blue = int((.5 - abs(perc - .5)) * 511)  # 0..0.5..1 -> 0..255..0
        #
        #     return QBrush(QColor(red, green, blue, 127))

        if role == cast(int, Qt.UserRole):
            print('WTF?')
            # return cast(
            #     T_FIELDS,
            #     getattr(
            #         self._data[row],
            #         FIELD_NAMES[column]))

        return None

    def sort(self,
             index: int,
             order: Qt.SortOrder = Qt.AscendingOrder) -> None:
        def key(info: Info) -> Union[date, Decimal, str]:
            e: Optional[Union[str, date, Decimal]]
            if index == 0:
                e = info.when
            elif index < 1 + len(ColumnHeader):
                e = info.columns[index - 1].howmuch
            else:
                e = f'TODO {index}'

            if e is None:
                return Decimal(0)

            return e

        self.layoutAboutToBeChanged()
        try:
            self._infos.sort(key=key, reverse=order == Qt.DescendingOrder)
        finally:
            self.layoutChanged()

    def load(self, infos: List[Info]) -> None:
        self.beginResetModel()
        try:
            self._set_infos(infos)
        finally:
            self.endResetModel()


class SortFilterViewModel(QSortFilterProxyModel):
    def __init__(self, infos: List[Info]) -> None:
        super().__init__()
        self.setSourceModel(ViewModel(self, infos))
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

    def filter_changed(self, text: str) -> None:
        self.setFilterFixedString(QRegularExpression.escape(text))

    def sort(self,
             column: int,
             order: Qt.SortOrder = Qt.AscendingOrder
             ) -> None:
        self.sourceModel().sort(column, order)

    # def selection_changed(self,
    #                       selection_model: QItemSelectionModel,
    #                       statusbar: QStatusBar) -> None:
    #
    #     addebiti_index = FIELD_NAMES.index('addebiti')
    #     accrediti_index = FIELD_NAMES.index('accrediti')
    #
    #     bigsum = 0
    #     for column, iop in ((addebiti_index, isub), (accrediti_index, iadd)):
    #         for index in selection_model.selectedRows(column):
    #             data = index.data(Qt.UserRole)
    #             if data is not None:
    #                 bigsum = iop(bigsum, data)
    #
    #     statusbar.showMessage(f'⅀ = {bigsum}')

    def load(self, infos: List[Info]) -> None:
        self.sourceModel().load(infos)
