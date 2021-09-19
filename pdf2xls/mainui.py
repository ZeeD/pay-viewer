from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from pkg_resources import resource_filename
from PySide6.QtGui import QStandardItemModel, QStandardItem, QWindow

MAINUI_UI_PATH = resource_filename('pdf2xls', 'mainui.ui')


class open_folder:
    def __init__(self, window: QWindow) -> None:
        self.window = window

    def __call__(self, *args, **kwargs) -> None:
        self.window.alert(2000)
        for arg in args:
            print(f'{arg=}')
        for karg, warg in kwargs.items():
            print(f'{karg=}, {warg=}')


def fetch_new_data(*args, **kwargs) -> None:
    for arg in args:
        print(f'{arg=}')
    for karg, warg in kwargs.items():
        print(f'{karg=}, {warg=}')


def main_ui() -> int:
    model = QStandardItemModel(14, 3)
    for row in range(model.rowCount()):
        for column in range(model.columnCount()):
            model.setItem(row, column, QStandardItem(f'{row=}, {column=}'))

    app = QApplication([__file__])
    window = QUiLoader().load(MAINUI_UI_PATH)
    window.tableView.setModel(model)
    window.actionOpen_folder.triggered.connect(open_folder(window))
    window.actionFetch_new_data.triggered.connect(fetch_new_data)
    window.show()
    return app.exec_()
