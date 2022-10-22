from typing import cast
from typing import Optional

from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QWidget

from .constants import FREEZE_TABLE_VIEW_UI_PATH


class TableViewUI(QWidget):
    left: QTableView
    right: QTableView


class FreezeTableView(QWidget):

    def __init__(self,
                 parent: Optional[QWidget],
                 model: QAbstractItemModel) -> None:
        super().__init__(parent)
        content = cast(TableViewUI, QUiLoader().load(FREEZE_TABLE_VIEW_UI_PATH))
        self._left = content.left
        self._right = content.right
        self._model = model

        layout = QGridLayout(self)
        layout.addWidget(content)
        self.setLayout(layout)

        self._left.setModel(model)
        self._right.setModel(model)

        # hide/show columns on model reset
        self._model.modelReset.connect(self._reset_columns)  # type: ignore

        # link vertical scroll
        self._right.verticalScrollBar().valueChanged.connect(# type: ignore
            self._left.verticalScrollBar().setValue)
        self._left.verticalScrollBar().valueChanged.connect(# type: ignore
            self._right.verticalScrollBar().setValue)

        # share and expose selection model
        self._selection_model = self._right.selectionModel()
        self._left.setSelectionModel(self._selection_model)

    def selectionModel(self) -> QItemSelectionModel:
        return self._selection_model

    def _reset_columns(self) -> None:
        # hide all-but-first column in left, first column in right
        for col in range(self._model.columnCount()):
            self._left.setColumnHidden(col, col != 0)
            self._right.setColumnHidden(col,
                                        col == 0 or not any(self._model.data(self._model.index(row, col))
                                                            for row in range(self._model.rowCount())))

        # force sort
        self._left.sortByColumn(0, Qt.SortOrder.DescendingOrder)

        self._left.resizeColumnsToContents()
        self._right.resizeColumnsToContents()
