from PySide6.QtCore import QUrl
from PySide6.QtQuick import QQuickView
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QPushButton
from PySide6.QtWidgets import QVBoxLayout
from PySide6.QtWidgets import QWidget


class dump:
    def __init__(self, view):
        self.view = view

    def __call__(self, status):
        print(f'{status=}')
        if status is QQuickView.Error:
            for error in self.view.errors():
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
container = QWidget.createWindowContainer(view)
container.setMinimumSize(100, 10)
layout.addWidget(container)

range_slider = view.rootObject()
range_slider.first_moved.connect(lambda first_value: print(f'{first_value=}'))
range_slider.second_moved.connect(lambda second_value: print(f'{second_value=}'))

dialog.show()
raise SystemExit(app.exec())
