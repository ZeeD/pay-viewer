from os import environ
from pathlib import Path
from typing import TYPE_CHECKING
from typing import cast

from guilib.searchsheet.widget import SearchSheet

if 'QT_API' not in environ:
    environ['QT_API'] = 'pyside6'

from qtpy.QtCore import QCoreApplication
from qtpy.QtCore import Qt
from qtpy.QtGui import QAction
from qtpy.QtUiTools import QUiLoader
from qtpy.QtWidgets import QApplication
from qtpy.QtWidgets import QDialog
from qtpy.QtWidgets import QDialogButtonBox
from qtpy.QtWidgets import QFileDialog
from qtpy.QtWidgets import QGridLayout
from qtpy.QtWidgets import QLineEdit
from qtpy.QtWidgets import QMainWindow
from qtpy.QtWidgets import QMessageBox
from qtpy.QtWidgets import QToolButton
from qtpy.QtWidgets import QWidget

from payviewer.chartwidget.chartwidget import ChartWidget
from payviewer.constants import MAINUI_UI_PATH
from payviewer.constants import SETTINGSUI_UI_PATH
from payviewer.freezetableview import FreezeTableView
from payviewer.loader import NoHistoryError
from payviewer.modelgui import SeriesModel
from payviewer.qwtchartwidget.qwtchartwidget import QwtChartVidget
from payviewer.removejsons import remove_jsons
from payviewer.settings import Settings
from payviewer.viewmodel import SortFilterViewModel
from payviewer.writer.csvwriter import CsvWriter

if TYPE_CHECKING:
    from qtpy.QtCore import QItemSelection


class Settingsui(QDialog):
    usernameLineEdit: QLineEdit  # noqa: N815
    passwordLineEdit: QLineEdit  # noqa: N815
    dataPathLineEdit: QLineEdit  # noqa: N815
    buttonBox: QDialogButtonBox  # noqa: N815
    toolButton: QToolButton  # noqa: N815


def new_settingsui(settings: Settings) -> Settingsui:
    def save_settings() -> None:
        settings.username = settingsui.usernameLineEdit.text()
        settings.password = settingsui.passwordLineEdit.text()
        settings.data_path = settingsui.dataPathLineEdit.text()

    def open_folder() -> None:
        settingsui.dataPathLineEdit.setText(QFileDialog.getExistingDirectory())

    settingsui = cast(Settingsui, QUiLoader().load(SETTINGSUI_UI_PATH))
    settingsui.usernameLineEdit.setText(settings.username)
    settingsui.passwordLineEdit.setText(settings.password)
    settingsui.dataPathLineEdit.setText(settings.data_path)

    settingsui.buttonBox.accepted.connect(save_settings)
    settingsui.toolButton.clicked.connect(open_folder)

    return settingsui


class Mainui(QMainWindow):
    xls: QWidget
    chart_money: QWidget
    chart_ferie: QWidget
    chart_rol: QWidget
    qwt_chart_money: QWidget
    lineEdit: QLineEdit  # noqa: N815
    actionCleanup: QAction  # noqa: N815
    actionSettings: QAction  # noqa: N815
    actionUpdate: QAction  # noqa: N815
    actionExport: QAction  # noqa: N815
    gridLayout_1: QGridLayout  # noqa: N815


def new_mainui(
    settings: Settings, model: SortFilterViewModel, settingsui: Settingsui
) -> QWidget:
    def update_helper(
        *, only_local: bool = False, force_pdf: bool = True
    ) -> None:
        try:
            model.update(only_local=only_local, force_pdf=force_pdf)
        except NoHistoryError:
            resp = QMessageBox.question(mainui, 'pdf2xls', 'Should load pdf?')
            if resp == QMessageBox.StandardButton.Yes:
                model.update(only_local=only_local, force_pdf=True)

    def update_status_bar(
        _selected: 'QItemSelection', _deselected: 'QItemSelection'
    ) -> None:
        model.selection_changed(selection_model, mainui.statusBar())

    def remove_jsons_helper() -> None:
        remove_jsons(settings.data_path)
        QMessageBox.information(mainui, 'pdf2xls', 'Cleanup complete')

    def export_helper() -> None:
        writer = CsvWriter(Path('/home/zed/Desktop/pdf2xls.csv'))
        writer.write_infos(model.get_rows())

    mainui = cast(Mainui, QUiLoader().load(MAINUI_UI_PATH))

    # replace table_view
    table_view = FreezeTableView(mainui.xls, model)
    sheet = SearchSheet(mainui.xls, table_view=table_view)
    sheet.set_model(model)
    mainui.gridLayout_1.addWidget(sheet, 0, 0)
    mainui.tableView = sheet
    # replace table_view

    selection_model = mainui.tableView.selection_model()
    selection_model.selectionChanged.connect(update_status_bar)

    chart_widget_money = ChartWidget(model, mainui, SeriesModel.money)
    mainui.chart_money.layout().addWidget(chart_widget_money)

    chart_widget_ferie = ChartWidget(model, mainui, SeriesModel.ferie)
    mainui.chart_ferie.layout().addWidget(chart_widget_ferie)

    chart_widget_rol = ChartWidget(model, mainui, SeriesModel.rol)
    mainui.chart_rol.layout().addWidget(chart_widget_rol)

    qwt_chart_widget_money = QwtChartVidget(model, mainui, SeriesModel.money)
    mainui.qwt_chart_money.layout().addWidget(qwt_chart_widget_money)

    # mainui.lineEdit.textChanged.connect(model.setFilterWildcard)

    mainui.actionUpdate.triggered.connect(update_helper)
    mainui.actionSettings.triggered.connect(settingsui.show)
    mainui.actionCleanup.triggered.connect(remove_jsons_helper)
    mainui.actionExport.triggered.connect(export_helper)
    settingsui.accepted.connect(update_helper)

    # QShortcut(QKeySequence('Ctrl+F'), mainui).activated.connect(
    # mainui.lineEdit.setFocus
    # )
    # QShortcut(QKeySequence('Esc'), mainui).activated.connect(
    # lambda: mainui.lineEdit.setText('')
    # )

    # on startup load only from local, and ask if you really want
    update_helper(only_local=True, force_pdf=False)

    return mainui


def main() -> None:
    QCoreApplication.setAttribute(
        Qt.ApplicationAttribute.AA_ShareOpenGLContexts
    )

    app = QApplication([__file__])
    settings = Settings()
    model = SortFilterViewModel(settings)
    settingsui = new_settingsui(settings)
    mainui = new_mainui(settings, model, settingsui)

    mainui.show()

    raise SystemExit(app.exec())
