from os import name
from typing import Final

from pkg_resources import resource_filename


def _resource(filename: str) -> str:
    return resource_filename('pdf2xls', f'resources/{filename}')


MAINUI_UI_PATH: Final = _resource('mainui.ui')
SETTINGSUI_UI_PATH: Final = _resource('settingsui.ui')
CHARTSLIDER_QML_PATH: Final = _resource('chartslider.qml')
CHARTHOVERUI_UI_PATH: Final = _resource('charthoverui.ui')
FREEZE_TABLE_VIEW_UI_PATH: Final = _resource('freeze_table_view.ui')

TEMPLATE_PATH: Final = _resource('tabula-template.json')
GECKODRIVER_PATH: Final = _resource('geckodriver' if name == 'posix' else 'geckodriver.exe')

SETTINGS_USERNAME: Final = 'username'
SETTINGS_PASSWORD: Final = 'password'
SETTINGS_DATA_PATH: Final = 'dataPath'
