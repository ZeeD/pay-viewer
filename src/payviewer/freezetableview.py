from typing import cast
from typing import override

from guilib.doubler.doubler import Doubler
from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QItemSelectionModel
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QWidget

from payviewer.constants import FREEZE_TABLE_VIEW_UI_PATH


class TableViewUI(QWidget):
    left: QTableView
    right: QTableView


class FreezeTableView(Doubler[QTableView], QAbstractItemView):
    def __init__(
        self,
        parent: QWidget | None,
        model: QAbstractItemModel,
        fixed_columns: int = 1,
    ) -> None:
        QAbstractItemView.__init__(self, parent)
        self.fixed_columns = fixed_columns
        content = cast(
            TableViewUI, QUiLoader(parent).load(FREEZE_TABLE_VIEW_UI_PATH)
        )
        Doubler.__init__(self, content.left, content.right)
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
            self._left.verticalScrollBar().setValue
        )
        self._left.verticalScrollBar().valueChanged.connect(
            self._right.verticalScrollBar().setValue
        )

        # share and expose selection model
        self._selection_model = self._right.selectionModel()
        self._left.setSelectionModel(self._selection_model)

        # expose click event
        self._left.clicked.connect(self.clicked.emit)
        self._right.clicked.connect(self.clicked.emit)

    @override
    def selectionModel(self) -> QItemSelectionModel:
        return self._selection_model

    def _reset_columns(self) -> None:
        # hide all-but-first column in left, first column in right
        for col in range(self._model.columnCount()):
            self._left.setColumnHidden(col, col >= self.fixed_columns)
            self._right.setColumnHidden(
                col,
                col < self.fixed_columns
                or not any(
                    self._model.data(self._model.index(row, col))
                    for row in range(self._model.rowCount())
                ),
            )

        # force sort
        for i in range(self.fixed_columns, -1, -1):
            self._left.sortByColumn(
                i, Qt.SortOrder.DescendingOrder
            )  # @UndefinedVariable

        self._left.resizeColumnsToContents()
        self._right.resizeColumnsToContents()

        self._right.horizontalHeader().setSectionsMovable(True)
