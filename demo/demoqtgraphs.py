from pathlib import Path

from PySide6.QtGui import QGuiApplication
from PySide6.QtQuick import QQuickView


def main() -> None:
    app = QGuiApplication([])

    viewer = QQuickView()
    viewer.setTitle('my title')
    viewer.setSource(str(Path(__file__).with_name('demoqtgraphs.qml')))
    viewer.setResizeMode(QQuickView.ResizeMode.SizeRootObjectToView)
    viewer.setColor('black')
    viewer.show()

    app.exec()

if __name__ == '__main__':
    main()
