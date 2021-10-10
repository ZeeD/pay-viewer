from PySide6.QtWidgets import QApplication
from PySide6.QtUiTools import QUiLoader
from pkg_resources import resource_filename
from PySide6.QtGui import QStandardItemModel, QStandardItem, QWindow

from .automation import try_fetch_new_data
from datetime import date

MAINUI_UI_PATH = resource_filename('pdf2xls', 'mainui.ui')


class open_folder:
    def __init__(self, window: QWindow) -> None:
        self.window = window

    def __call__(self) -> None:
        pass


class fetch_new_data:
    def __init__(self) -> None:
        pass

    def __call__(self) -> None:
        last = date(2021, 8, 1)
        new_data = try_fetch_new_data(last)
        if new_data:
            pass  # TODO reload ui? boh


def main_ui() -> int:
    model = QStandardItemModel(14, 3)
    for row in range(model.rowCount()):
        for column in range(model.columnCount()):
            model.setItem(row, column, QStandardItem(f'{row=}, {column=}'))

    app = QApplication([__file__])
    window = QUiLoader().load(MAINUI_UI_PATH)
    window.tableView.setModel(model)
    window.actionOpen_folder.triggered.connect(open_folder(window))
    window.actionFetch_new_data.triggered.connect(fetch_new_data())
    window.show()
    return app.exec_()
