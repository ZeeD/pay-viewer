from os import name
from pathlib import Path
from typing import Final

_RESOURCES: Final = Path(__file__).parent / 'resources'


MAINUI_UI_PATH: Final = _RESOURCES / 'mainui.ui'
SETTINGSUI_UI_PATH: Final = _RESOURCES / 'settingsui.ui'
CHARTSLIDER_QML_PATH: Final = _RESOURCES / 'chartslider.qml'
CHARTHOVERUI_UI_PATH: Final = _RESOURCES / 'charthoverui.ui'
FREEZE_TABLE_VIEW_UI_PATH: Final = _RESOURCES / 'freeze_table_view.ui'

TEMPLATE_PATH: Final = _RESOURCES / 'tabula-template.json'
GECKODRIVER_PATH: Final = _RESOURCES / (
    'geckodriver' if name == 'posix' else 'geckodriver.exe'
)


SETTINGS_USERNAME: Final = 'username'
SETTINGS_PASSWORD: Final = 'password'
SETTINGS_DATA_PATH: Final = 'dataPath'
