from datetime import date
from typing import cast

from PySide6.QtCore import QSettings
from PySide6.QtGui import QStandardItemModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QWidget
from os import listdir

from .automation import try_fetch_new_data
from .constants import MAINUI_UI_PATH
from .constants import SETTINGS_DATA_PATH
from .constants import SETTINGS_PASSWORD
from .constants import SETTINGS_USERNAME
from .constants import SETTINGSUI_UI_PATH
from .loader import load
from .viewmodel import SortFilterViewModel


def new_model(settings: QSettings) -> QStandardItemModel:
    def load_current_data() -> None:
        infos = load(cast(str, settings.value(SETTINGS_DATA_PATH)))
        model.load(infos)

    def update() -> None:
        data_path = cast(str, settings.value(SETTINGS_DATA_PATH))
        max_year = max(fn for fn in listdir(data_path) if '.' not in fn)
        last_pdf = max(fn for fn in listdir(f'{data_path}/{max_year}')
                       if fn.endswith('.pdf'))
        year, month = map(int, last_pdf.split('.', 1)[0].split('_', 2)[1:])
        last = date(year, month, 1)
        new_data = try_fetch_new_data(last, settings)
        if new_data:
            load_current_data()

    model = SortFilterViewModel([])
    load_current_data()

    model.update = update
    return model


def new_settingsui(settings: QSettings) -> QWidget:
    def save_settings() -> None:
        settings.setValue(SETTINGS_USERNAME,
                          settingsui.usernameLineEdit.text())
        settings.setValue(SETTINGS_PASSWORD,
                          settingsui.passwordLineEdit.text())
        settings.setValue(SETTINGS_DATA_PATH,
                          settingsui.dataPathLineEdit.text())

    def open_folder() -> None:
        settingsui.dataPathLineEdit.setText(QFileDialog.getExistingDirectory())

    settingsui = QUiLoader().load(SETTINGSUI_UI_PATH)
    settingsui.usernameLineEdit.setText(settings.value(SETTINGS_USERNAME))
    settingsui.passwordLineEdit.setText(settings.value(SETTINGS_PASSWORD))
    settingsui.dataPathLineEdit.setText(settings.value(SETTINGS_DATA_PATH))

    settingsui.buttonBox.accepted.connect(save_settings)
    settingsui.toolButton.clicked.connect(open_folder)

    return settingsui


def new_mainui(model: QStandardItemModel, settingsui: QWidget) -> QWidget:
    mainui = QUiLoader().load(MAINUI_UI_PATH)
    mainui.tableView.setModel(model)
    mainui.show()

    mainui.actionUpdate.triggered.connect(model.update)
    mainui.actionSettings.triggered.connect(settingsui.show)
    settingsui.accepted.connect(model.update)

    return mainui


def main_ui() -> int:
    app = QApplication([__file__])

    settings = QSettings('ZeeD', 'pdf2xls')
    model = new_model(settings)
    settingsui = new_settingsui(settings)
    mainui = new_mainui(model, settingsui)
    mainui = mainui

    return app.exec_()
