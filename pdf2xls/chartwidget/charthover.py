from decimal import Decimal
from typing import cast
from typing import Optional

from PySide6.QtCore import QPointF
from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtWidgets import QGraphicsLayoutItem
from PySide6.QtWidgets import QGraphicsLinearLayout
from PySide6.QtWidgets import QGraphicsProxyWidget
from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtWidgets import QLabel


class ChartHover(QGraphicsWidget):

    def __init__(self, parent: Optional[QGraphicsItem]=None) -> None:
        super().__init__(parent)
        self.items: list[QGraphicsLayoutItem] = []
        self.setLayout(QGraphicsLinearLayout(Qt.Orientation.Vertical))
        self.setZValue(11)

    def set_howmuchs(self, howmuchs: dict[str, Decimal], pos: QPointF) -> None:
        if pos == self.pos():
            return

        layout = cast(QGraphicsLinearLayout, self.layout())
        for item in self.items:
            layout.removeItem(item)
        self.items.clear()
        for name, howmuch in howmuchs.items():
            item = QGraphicsProxyWidget(self)
            item.setWidget(QLabel(f'{name}: {howmuch}'))
            layout.addItem(item)
            self.items.append(item)
        self.setPos(pos)
