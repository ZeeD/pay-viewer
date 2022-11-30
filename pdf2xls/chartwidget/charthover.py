from decimal import Decimal
from typing import cast
from typing import Optional

from PySide6.QtCore import QPointF, Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QGraphicsItem, QFormLayout
from PySide6.QtWidgets import QGraphicsLinearLayout
from PySide6.QtWidgets import QGraphicsProxyWidget
from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget

from ..constants import CHARTHOVERUI_UI_PATH
from datetime import date
from PySide6.QtGui import QColor


class ChartHoverUI(QWidget):
    label: QLabel
    formLayout: QFormLayout


class ChartHover(QGraphicsWidget):

    def __init__(self, parent: Optional[QGraphicsItem]=None) -> None:
        super().__init__(parent)
        self.setLayout(QGraphicsLinearLayout(Qt.Orientation.Vertical))
        self.setZValue(11)

        self.widget = cast(
            ChartHoverUI, QUiLoader().load(CHARTHOVERUI_UI_PATH))

        item = QGraphicsProxyWidget(self)
        item.setWidget(self.widget)

    def set_howmuchs(self,
                     when: date,
                     howmuchs: dict[str, tuple[QColor, Decimal]],
                     pos: QPointF) -> None:
        if pos == self.pos():
            return

        self.widget.label.setText(f'{when:%B %Y}')

        # self.widget.formLayout.
        #
        # for item in self.items:
        # layout.removeItem(item)
        # self.items.clear()
        # for name, howmuch in howmuchs.items():
        # item = QGraphicsProxyWidget(self)
        # item.setWidget(QLabel(f'{name}: {howmuch}'))
        # layout.addItem(item)
        # self.items.append(item)

        self.setPos(pos)
