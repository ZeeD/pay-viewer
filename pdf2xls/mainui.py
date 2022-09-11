from PySide6.QtCore import QItemSelection
from PySide6.QtGui import QKeySequence
from PySide6.QtGui import QShortcut
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QWidget

from .chartwidget.chartwidget import ChartWidget
from .constants import MAINUI_UI_PATH
from .constants import SETTINGSUI_UI_PATH
from .freezetableview import FreezeTableView
from .loader import NoHistoryException
from .removejsons import remove_jsons
from .settings import Settings
from .viewmodel import SortFilterViewModel


def new_settingsui(settings: Settings) -> QWidget:
    def save_settings() -> None:
        settings.username = settingsui.usernameLineEdit.text()
        settings.password = settingsui.passwordLineEdit.text()
        settings.data_path = settingsui.dataPathLineEdit.text()

    def open_folder() -> None:
        settingsui.dataPathLineEdit.setText(QFileDialog.getExistingDirectory())

    settingsui = QUiLoader().load(SETTINGSUI_UI_PATH)
    settingsui.usernameLineEdit.setText(settings.username)
    settingsui.passwordLineEdit.setText(settings.password)
    settingsui.dataPathLineEdit.setText(settings.data_path)

    settingsui.buttonBox.accepted.connect(save_settings)
    settingsui.toolButton.clicked.connect(open_folder)

    return settingsui


def new_mainui(settings: Settings,
               model: SortFilterViewModel,
               settingsui: QWidget) -> QWidget:
    def update_helper(*,
                      only_local: bool = False,
                      force_pdf: bool = True) -> None:
        try:
            model.update(only_local=only_local, force_pdf=force_pdf)
        except NoHistoryException:
            resp = QMessageBox.question(mainui, 'pdf2xls', 'Should load pdf?')
            if resp == QMessageBox.StandardButton.Yes:
                model.update(only_local=only_local, force_pdf=True)

    def update_status_bar(_selected: QItemSelection,
                          _deselected: QItemSelection) -> None:
        model.selectionChanged(selection_model, mainui.statusBar())

    def remove_jsons_helper() -> None:
        remove_jsons(settings.data_path)
        QMessageBox.information(mainui, 'pdf2xls', 'Cleanup complete')

    mainui = QUiLoader().load(MAINUI_UI_PATH)

    # replace tableView
    tableView = FreezeTableView(mainui.tableView.parent(), model)
    mainui.gridLayout_1.replaceWidget(mainui.tableView, tableView)
    mainui.tableView.deleteLater()
    mainui.tableView = tableView
    # replace tableView

    selection_model = mainui.tableView.selectionModel()
    selection_model.selectionChanged.connect(update_status_bar)

    # chart
    # filled_group_box = FilledGroupBox(mainui, model)
    # mainui.tab_2.layout().addWidget(filled_group_box)
    #
    # chart_view = ChartView(mainui, model)
    # mainui.tab_2.layout().addWidget(chart_view)
    # chart

    # chart 3
    chart_widget = ChartWidget(model, mainui)
    mainui.chart.layout().addWidget(chart_widget)
    # chart 3

    mainui.lineEdit.textChanged.connect(model.filterChanged)

    mainui.actionUpdate.triggered.connect(update_helper)
    mainui.actionSettings.triggered.connect(settingsui.show)
    mainui.actionCleanup.triggered.connect(remove_jsons_helper)
    settingsui.accepted.connect(update_helper)

    QShortcut(QKeySequence(mainui.tr('Ctrl+F')),
              mainui).activated.connect(mainui.lineEdit.setFocus)
    QShortcut(QKeySequence(mainui.tr('Esc')),
              mainui).activated.connect(lambda: mainui.lineEdit.setText(''))

    # on startup load only from local, and ask if you really want
    update_helper(only_local=True, force_pdf=False)

    return mainui


def main() -> None:
    app = QApplication([__file__])

    settings = Settings()
    model = SortFilterViewModel(settings)
    settingsui = new_settingsui(settings)
    mainui = new_mainui(settings, model, settingsui)

    mainui.show()

    raise SystemExit(app.exec())
