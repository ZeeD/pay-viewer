from decimal import Decimal
from typing import Optional, cast

from PySide6.QtCore import Qt
from PySide6.QtWidgets import QGraphicsItem
from PySide6.QtWidgets import QGraphicsLayoutItem
from PySide6.QtWidgets import QGraphicsLinearLayout
from PySide6.QtWidgets import QGraphicsProxyWidget
from PySide6.QtWidgets import QGraphicsWidget
from PySide6.QtWidgets import QLabel


class ChartHover(QGraphicsWidget):
    def __init__(self, parent: Optional[QGraphicsItem] = None) -> None:
        super().__init__(parent)
        self.items: list[QGraphicsLayoutItem] = []
        self.setLayout(QGraphicsLinearLayout(Qt.Vertical))

    def set_howmuchs(self, howmuchs: dict[str, Decimal]) -> None:
        layout = cast(QGraphicsLinearLayout, self.layout())
        for item in self.items:
            layout.removeItem(item)
        self.items.clear()
        for name, howmuch in howmuchs.items():
            item = QGraphicsProxyWidget(self)
            item.setWidget(QLabel(f'{name}: {howmuch}'))
            layout.addItem(item)
            self.items.append(item)
