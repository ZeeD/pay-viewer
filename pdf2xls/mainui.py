from datetime import date
from os import listdir

from PySide6.QtGui import QStandardItemModel
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication
from PySide6.QtWidgets import QFileDialog
from PySide6.QtWidgets import QMessageBox
from PySide6.QtWidgets import QWidget

from .automation import try_fetch_new_data
from .constants import MAINUI_UI_PATH
from .constants import SETTINGSUI_UI_PATH
from .loader import NoHistoryException
from .loader import load
from .removejsons import remove_jsons
from .settings import Settings
from .viewmodel import SortFilterViewModel


def new_model(settings: Settings) -> QStandardItemModel:
    def update(*, only_local: bool, force_pdf: bool) -> None:
        if only_local:
            new_data = True
        else:
            data_path = settings.data_path
            max_year = max(fn for fn in listdir(data_path) if '.' not in fn)
            last_pdf = max(fn for fn in listdir(f'{data_path}/{max_year}')
                           if fn.endswith('.pdf'))
            year, month = map(int, last_pdf.split('.', 1)[0].split('_', 2)[1:])
            last = date(year, month, 1)
            new_data = try_fetch_new_data(last, settings)
        if new_data:
            model.load(load(settings.data_path, force=force_pdf))

    model = SortFilterViewModel([])
    model.update = update
    return model


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


def new_mainui(model: QStandardItemModel,
               settingsui: QWidget,
               settings: Settings) -> QWidget:
    def model_update_helper(*, only_local: bool = False) -> None:
        try:
            model.update(only_local=only_local, force_pdf=False)
        except NoHistoryException:
            resp = QMessageBox.question(mainui, 'pdf2xls', 'Should load pdf?')
            if resp == QMessageBox.StandardButton.Yes:
                model.update(only_local=only_local, force_pdf=True)

    def remove_jsons_helper() -> None:
        remove_jsons(settings.data_path)
        QMessageBox.information(mainui, 'pdf2xls', 'Cleanup complete')

    mainui = QUiLoader().load(MAINUI_UI_PATH)
    mainui.tableView.setModel(model)
    mainui.show()

    mainui.actionUpdate.triggered.connect(model_update_helper)
    mainui.actionSettings.triggered.connect(settingsui.show)
    mainui.actionCleanup.triggered.connect(remove_jsons_helper)
    settingsui.accepted.connect(model.update)

    # on startup load only from local
    model_update_helper(only_local=True)

    return mainui


def main() -> int:
    app = QApplication([__file__])

    settings = Settings()
    model = new_model(settings)
    settingsui = new_settingsui(settings)
    mainui = new_mainui(model, settingsui, settings)
    mainui = mainui

    return app.exec_()
