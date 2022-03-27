from typing import Optional

from PySide6.QtCore import QAbstractItemModel, QItemSelectionModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QWidget

from .constants import FREEZE_TABLE_VIEW_UI_PATH


class FreezeTableView(QWidget):
    def __init__(self,
                 parent: Optional[QWidget],
                 model: QAbstractItemModel) -> None:
        super().__init__(parent)
        content = QUiLoader().load(FREEZE_TABLE_VIEW_UI_PATH)
        self._left: QTableView = content.left
        self._right: QTableView = content.right
        self._model = model

        layout = QGridLayout(self)
        layout.addWidget(content)
        self.setLayout(layout)

        self._left.setModel(model)
        self._right.setModel(model)

        # hide/show columns on model reset
        self._model.modelReset.connect(self._reset_columns)

        # link vertical scroll
        self._right.verticalScrollBar().valueChanged.connect(
            self._left.verticalScrollBar().setValue)

        # share and expose selection model
        self._selection_model = self._right.selectionModel()
        self._left.setSelectionModel(self._selection_model)

    def selectionModel(self) -> QItemSelectionModel:
        return self._selection_model

    def _reset_columns(self) -> None:
        # hide all-but-first column in left, first column in right
        for col in range(self._model.columnCount()):
            self._left.setColumnHidden(col, col != 0)
            self._right.setColumnHidden(col, col == 0)
