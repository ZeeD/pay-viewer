from functools import partial
from logging import INFO
from logging import basicConfig
from pathlib import Path
from typing import TYPE_CHECKING
from typing import cast

from guilib.searchsheet.widget import SearchSheet
from PySide6.QtCore import QCoreApplication
from PySide6.QtCore import QModelIndex
from PySide6.QtCore import Qt
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QDialog
from PySide6.QtWidgets import QDialogButtonBox
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QGridLayout
from PySide6.QtWidgets import QLineEdit
from PySide6.QtWidgets import QMainWindow
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QToolButton
from PySide6.QtWidgets import QWidget

from payviewer.chartwidget.chartwidget import ChartWidget
from payviewer.constants import MAINUI_UI_PATH
from payviewer.constants import SETTINGSUI_UI_PATH
from payviewer.freezetableview import FreezeTableView
from payviewer.loader import NoHistoryError
from payviewer.modelgui import SeriesModel
from payviewer.pdfviewer import view_pdf
from payviewer.qwtchartwidget.qwtchartwidget import QwtChartVidget
from payviewer.removejsons import remove_jsons
from payviewer.settings import Settings
from payviewer.viewmodel import PATH_ROLE
from payviewer.viewmodel import SortFilterViewModel
from payviewer.writer.csvwriter import CsvWriter

if TYPE_CHECKING:
    from PySide6.QtCore import QItemSelection
    from PySide6.QtGui import QAction
    from PySide6.QtWidgets import QTableView


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

    settingsui = cast('Settingsui', QUiLoader().load(SETTINGSUI_UI_PATH))
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
    qwt_chart_ticket: QWidget
    lineEdit: QLineEdit  # noqa: N815
    actionCleanup: 'QAction'  # noqa: N815
    actionSettings: 'QAction'  # noqa: N815
    actionUpdate: 'QAction'  # noqa: N815
    actionExport: 'QAction'  # noqa: N815
    gridLayout_1: QGridLayout  # noqa: N815
    tableView: QWidget  # noqa: N815
    qwt_chart_ferie_rol: QWidget


WIDGETS: list[QWidget] = []


def onclick(model: SortFilterViewModel, index: QModelIndex) -> None:
    if index.column() != 0:
        return
    data = model.data(index, PATH_ROLE)
    widget = view_pdf(data)
    widget.show()
    WIDGETS.append(widget)


def new_mainui(  # noqa: C901, PLR0915
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
        QMessageBox.information(
            mainui,
            'pdf2xls',
            'Cleanup complete',
            QMessageBox.StandardButton.Close,
        )

    def export_helper() -> None:
        writer = CsvWriter(Path('/home/zed/Desktop/pdf2xls.csv'))
        writer.write_infos(model.get_rows())

    mainui = cast('Mainui', QUiLoader().load(MAINUI_UI_PATH))

    # replace table_view
    table_view = FreezeTableView(mainui.xls, model)
    table_view.clicked.connect(partial(onclick, model))

    sheet = SearchSheet(mainui.xls, table_view=cast('QTableView', table_view))
    sheet.set_model(model)
    mainui.gridLayout_1.addWidget(sheet, 0, 0)
    mainui.tableView = sheet
    # replace table_view

    selection_model = mainui.tableView.selection_model()
    selection_model.selectionChanged.connect(update_status_bar)

    money_layout = mainui.chart_money.layout()
    if money_layout is None:
        raise ValueError
    money_layout.addWidget(ChartWidget(model, mainui, SeriesModel.money))

    ferie_layout = mainui.chart_ferie.layout()
    if ferie_layout is None:
        raise ValueError
    ferie_layout.addWidget(ChartWidget(model, mainui, SeriesModel.ferie))

    rol_layout = mainui.chart_rol.layout()
    if rol_layout is None:
        raise ValueError
    rol_layout.addWidget(ChartWidget(model, mainui, SeriesModel.rol))

    money_layout_qwt = mainui.qwt_chart_money.layout()
    if money_layout_qwt is None:
        raise ValueError
    money_layout_qwt.addWidget(QwtChartVidget(model, mainui, SeriesModel.money))

    ticket_layout = mainui.qwt_chart_ticket.layout()
    if ticket_layout is None:
        raise ValueError
    ticket_layout.addWidget(QwtChartVidget(model, mainui, SeriesModel.ticket))

    ferie_rol_layout = mainui.qwt_chart_ferie_rol.layout()
    if ferie_rol_layout is None:
        raise ValueError
    ferie_rol_layout.addWidget(
        QwtChartVidget(model, mainui, SeriesModel.ferie_rol)
    )

    mainui.actionUpdate.triggered.connect(update_helper)
    mainui.actionSettings.triggered.connect(settingsui.show)
    mainui.actionCleanup.triggered.connect(remove_jsons_helper)
    mainui.actionExport.triggered.connect(export_helper)
    settingsui.accepted.connect(update_helper)

    # on startup load only from local, and ask if you really want
    update_helper(only_local=True, force_pdf=False)

    return mainui


def main() -> None:
    basicConfig(level=INFO, format='%(message)s')
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
