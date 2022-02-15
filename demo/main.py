from PySide6.QtCore import QUrl
from PySide6.QtQuick import QQuickItem
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class dump:
    def __init__(self, qqv: QQuickView):
        self.qqv = qqv

    def __call__(self, status: QQuickView.Status) -> None:
        print(f'{status=}')
        if status is QQuickView.Error:
            for error in self.qqv.errors():
                print(f'{error=}')


app = QApplication()
dialog = QDialog()
layout = QVBoxLayout()
dialog.setLayout(layout)

button = QPushButton('click')
layout.addWidget(button)
button.clicked.connect(lambda: print('clock'))

view = QQuickView()
view.statusChanged.connect(dump(view))
view.setResizeMode(QQuickView.SizeRootObjectToView)
view.setSource(QUrl.fromLocalFile('view.qml'))
range_slider: QQuickItem = view.rootObject()
range_slider.first_moved.connect(lambda first_value: print(f'{first_value=}'))
range_slider.second_moved.connect(lambda second_value: print(f'{second_value=}'))
range_slider.setProperty('from', 0.)
range_slider.setProperty('to', 1000.)
container = QWidget.createWindowContainer(view)
container.setMinimumSize(100, 10)
layout.addWidget(container)


dialog.show()
raise SystemExit(app.exec())
