from datetime import date
from decimal import Decimal
from typing import cast

from qtpy.QtCore import QPointF
from qtpy.QtCore import QSizeF
from qtpy.QtCore import Qt
from qtpy.QtGui import QColor
from qtpy.QtUiTools import QUiLoader
from qtpy.QtWidgets import QFormLayout
from qtpy.QtWidgets import QGraphicsItem
from qtpy.QtWidgets import QGraphicsLinearLayout
from qtpy.QtWidgets import QGraphicsProxyWidget
from qtpy.QtWidgets import QGraphicsWidget
from qtpy.QtWidgets import QLabel
from qtpy.QtWidgets import QWidget

from constants import CHARTHOVERUI_UI_PATH


class ChartHoverUI(QWidget):
    label: QLabel
    ormLayout: QFormLayout  # noqa: N815


class ChartHover(QGraphicsWidget):
    def __init__(self, parent: QGraphicsItem | None = None) -> None:
        super().__init__(parent)
        self.setLayout(QGraphicsLinearLayout(Qt.Orientation.Vertical))
        self.setZValue(11)

        self.widget = cast(ChartHoverUI, QUiLoader().load(CHARTHOVERUI_UI_PATH))

        item = QGraphicsProxyWidget(self)
        item.setWidget(self.widget)
        self.keyToValueLabel: dict[str, QLabel] = {}

    def set_howmuchs(
        self,
        when: date,
        howmuchs: dict[str, tuple[QColor, Decimal]],
        pos: QPointF,
    ) -> None:
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
