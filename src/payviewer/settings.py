from typing import cast

from PySide6.QtCore import QSettings

from payviewer.constants import SETTINGS_DATA_PATH
from payviewer.constants import SETTINGS_PASSWORD
from payviewer.constants import SETTINGS_USERNAME


class Settings:
    def __init__(self) -> None:
        self.settings = QSettings('ZeeD', 'pdf2xls')

    @property
    def username(self) -> str:
        return cast(str, self.settings.value(SETTINGS_USERNAME))

    @username.setter
    def username(self, username: str) -> None:
        self.settings.setValue(SETTINGS_USERNAME, username)

    @property
    def password(self) -> str:
        return cast(str, self.settings.value(SETTINGS_PASSWORD))

    @password.setter
    def password(self, password: str) -> None:
        self.settings.setValue(SETTINGS_PASSWORD, password)

    @property
    def data_path(self) -> str:
        return cast(str, self.settings.value(SETTINGS_DATA_PATH))

    @data_path.setter
    def data_path(self, data_path: str) -> None:
        self.settings.setValue(SETTINGS_DATA_PATH, data_path)
