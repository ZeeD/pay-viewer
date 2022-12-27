from datetime import date
from decimal import Decimal
from typing import cast
from typing import Optional

from PySide6.QtCore import QPointF
from PySide6.QtCore import QSizeF
from PySide6.QtCore import Qt
from PySide6.QtGui import QColor
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QFormLayout
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtWidgets import QGraphicsLinearLayout
from PySide6.QtWidgets import QGraphicsProxyWidget
from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtWidgets import QLabel
from PySide6.QtWidgets import QWidget

from ..constants import CHARTHOVERUI_UI_PATH


class ChartHoverUI(QWidget):
    label: QLabel
    ormLayout: QFormLayout


class ChartHover(QGraphicsWidget):
    def __init__(self, parent: Optional[QGraphicsItem]=None) -> None:
        super().__init__(parent)
        self.setLayout(QGraphicsLinearLayout(Qt.Orientation.Vertical))
        self.setZValue(11)

        self.widget = cast(ChartHoverUI,
                           QUiLoader().load(CHARTHOVERUI_UI_PATH))

        item = QGraphicsProxyWidget(self)
        item.setWidget(self.widget)
        self.keyToValueLabel: dict[str, QLabel] = {}

    def set_howmuchs(self,
                     when: date,
                     howmuchs: dict[str, tuple[QColor, Decimal]],
                     pos: QPointF) -> None:
        if pos == self.pos():
            return

        self.widget.label.setText(f'{when:%B %Y}')

        for key, label in self.keyToValueLabel.items():
            if key not in howmuchs:
                self.widget.ormLayout.removeRow(label)
                del self.keyToValueLabel[key]
            else:
                _, v = howmuchs[key]
                label.setText(str(v))

        for key, (color, v) in howmuchs.items():
            if key in self.keyToValueLabel:
                continue
            label = QLabel(str(v), self.widget)
            label.setStyleSheet(f'background-color: {color.name()}')

            self.widget.ormLayout.addRow(key, label)
            self.keyToValueLabel[key] = label

        self.setPos(pos)

    def size(self) -> QSizeF:
        return QSizeF(self.widget.size())
