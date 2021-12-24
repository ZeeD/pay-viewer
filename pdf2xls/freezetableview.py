from PySide6.QtCore import QAbstractItemModel
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Qt
from PySide6.QtCore import Slot
from PySide6.QtGui import QResizeEvent
from PySide6.QtWidgets import QAbstractItemView
from PySide6.QtWidgets import QHeaderView
from PySide6.QtWidgets import QTableView
from PySide6.QtWidgets import QWidget


class FreezeTableView(QTableView):
    def __init__(self, parent: QWidget, model: QAbstractItemModel) -> None:
        super().__init__(parent)
        super().setModel(model)
        self.frozenTableView = QTableView(self)
        self.init()

        self.horizontalHeader().sectionResized.connect(self.updateSectionWidth)
        self.verticalHeader().sectionResized.connect(self.updateSectionHeight)
        self.frozenTableView.verticalScrollBar().valueChanged.connect(
            self.verticalScrollBar().setValue)
        self.verticalScrollBar().valueChanged.connect(
            self.frozenTableView.verticalScrollBar().setValue)

    def init(self) -> None:
        ftw = self.frozenTableView
        ftw.setModel(self.model())
        ftw.setFocusPolicy(Qt.NoFocus)
        ftw.verticalHeader().hide()
        ftw.horizontalHeader().setSectionResizeMode(QHeaderView.Fixed)
        self.viewport().stackUnder(ftw)

        if self.selectionModel():
            ftw.setSelectionModel(self.selectionModel())
        if self.model():
            for col in range(1, self.model().columnCount()):
                ftw.setColumnHidden(col, True)
        ftw.setColumnWidth(0, self.columnWidth(0))
        ftw.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ftw.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        ftw.show()
        self.updateFrozenTableGeometry()
        self.setHorizontalScrollMode(self.ScrollPerPixel)
        self.setVerticalScrollMode(self.ScrollPerPixel)
        ftw.setVerticalScrollMode(self.ScrollPerPixel)

    @Slot()
    def updateSectionWidth(self,
                           logicalIndex: int,
                           _oldSize: int,
                           newSize: int) -> None:
        if logicalIndex == 0:
            self.frozenTableView.setColumnWidth(0, newSize)
            self.updateFronzenTableGeometry()

    @Slot()
    def updateSectionHeight(self,
                            logicalIndex: int,
                            _oldSize: int,
                            newSize: int) -> None:
        self.frozenTableView.setRowHeight(logicalIndex, newSize)

    def resizeEvent(self, event: QResizeEvent) -> None:
        super().resizeEvent(event)
        self.updateFrozenTableGeometry()

    def moveCursor(self,
                   cursorAction: QAbstractItemView.CursorAction,
                   modifiers: Qt.KeyboardModifiers) -> QModelIndex:
        current = super().moveCursor(cursorAction, modifiers)
        if (cursorAction == QAbstractItemView.CursorAction.MoveLeft and
            current.column() > 0 and
            self.visualRect(current).topLeft().x() <
                self.frozenTableView.columnWidth(0)):
            newValue = (self.horizontalScrollBar().value() +
                        self.visualRect(current).topLeft().x() -
                        self.frozenTableView.columnWidth(0))
            self.horizontalScrollBar().setValue(newValue)

        return current

    def scrollTo(self,
                 index: QModelIndex,
                 hint: QAbstractItemView.ScrollHint
                 = QAbstractItemView.ScrollHint.EnsureVisible) -> None:
        if index.column() > 0:
            super().scrollTo(index, hint)

    def updateFrozenTableGeometry(self) -> None:
        self.frozenTableView.setGeometry(self.verticalHeader().width()
                                         + self.frameWidth(),
                                         self.frameWidth(),
                                         self.columnWidth(0),
                                         self.viewport().height()
                                         + self.horizontalHeader().height())
