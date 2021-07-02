from contextlib import contextmanager
# from .viewmodel import SortFilterViewModel
from pathlib import Path
from typing import Final
from typing import Iterator

from pkg_resources import resource_filename
from PySide2.QtCore import QItemSelection
from PySide2.QtUiTools import QUiLoader
from PySide2.QtWidgets import QApplication
from PySide2.QtWidgets import QErrorMessage
from PySide2.QtWidgets import QFileDialog
from PySide2.QtWidgets import QMainWindow

from .chartview import ChartView
from .model import loader

VIEWER_UI_PATH: Final = resource_filename('viewer', 'viewer.ui')


@contextmanager
def main_window(file_name: Path) -> Iterator[QMainWindow]:

    def update_status_bar(_selected: QItemSelection,
                          _deselected: QItemSelection) -> None:
        # view_model.selection_changed(selection_model, window.statusBar())
        pass

    def update_data() -> None:
        path, _ = QFileDialog.getOpenFileName(window)
        if not path:
            print('no path')
            return

        new_data = loader(path)
        try:
            # view_model.load(new_data)
            chart_view.load(new_data)
        except Exception as e:
            QErrorMessage(window).showMessage('\n'.join(map(str, e.args)))

    app = QApplication([__file__])

    window = QUiLoader().load(VIEWER_UI_PATH)

    data = loader(file_name)

    # view_model = SortFilterViewModel(window, data)
    # window.tableView.setModel(view_model)
    # selection_model = window.tableView.selectionModel()
    # selection_model.selectionChanged.connect(update_status_bar)

    # window.lineEdit.textChanged.connect(view_model.filter_changed)

    chart_view = ChartView(window, data)
    window.tab_2.layout().addWidget(chart_view)

    window.actionOpen.triggered.connect(update_data)

    try:
        yield window
    finally:
        app.exec_()
