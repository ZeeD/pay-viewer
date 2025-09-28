from datetime import UTC
from datetime import datetime
from logging import getLogger
from pathlib import Path
from shutil import move
from tempfile import TemporaryDirectory
from time import sleep
from typing import TYPE_CHECKING
from typing import Final
from typing import NamedTuple

from selenium.webdriver import Firefox
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located,
)
from selenium.webdriver.support.expected_conditions import url_contains
from selenium.webdriver.support.wait import WebDriverWait

from payviewer.constants import GECKODRIVER_PATH

if TYPE_CHECKING:
    from collections.abc import Iterable


NOV: Final = 11
DIC: Final = 12
TRED: Final = 13

LOGGER = getLogger(__name__)


class Date(NamedTuple):
    year: int
    month: int

    def get_year_months(self) -> 'Iterable[Date]':
        """Infinite generator of (year, month) from last."""
        d = self
        while True:
            if d.month == NOV:  # (year, 13) is extra month's salary
                d = Date(d.year, TRED)
            elif d.month == TRED:  # (year, 13) happens before (year, 12)
                d = Date(d.year, DIC)
            elif d.month == DIC:
                d = Date(d.year + 1, 1)
            else:
                d = Date(d.year, d.month + 1)

            yield d


def options(dtemp: str) -> Options:
    profile = FirefoxProfile()

    # disable Firefox's built-in PDF viewer
    profile.set_preference('pdfjs.disabled', value=True)

    # set download folder
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', dtemp)
    profile.set_preference(
        'browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream'
    )

    options = Options()
    options.profile = profile
    return options


def wait_download(dtemp: str) -> None:
    dptemp = Path(dtemp)
    LOGGER.info('wait_download (initial: %s)', list(dptemp.iterdir()))
    while not list(dptemp.iterdir()):
        sleep(0.5)
        LOGGER.info('wait_download [empty]')
    while any(fn.suffix == '.part' for fn in dptemp.iterdir()):
        sleep(0.5)
        LOGGER.info('wait_download [.part]')


def mv_pdf_from_tmp_to_data(
    dtemp: str, year: int, month: int, data_path: str
) -> None:
    Path(f'{data_path}/{year}').mkdir(parents=True, exist_ok=True)
    dptemp = Path(dtemp)

    LOGGER.info('files in dtemp:')
    dtempfns = list(dptemp.iterdir())
    for dtempfn in dtempfns:
        LOGGER.info('\t%s/%s', dtemp, dtempfn)
        if f'Cedolini_{year}_{month:02}.pdf' == dtempfn.name:
            LOGGER.info('\t(matched)')
            src = f'{dtemp}/Cedolini_{year}_{month:02}.pdf'
            break
    else:
        LOGGER.warning('\t(NOT matched)')
        src = f'{dtemp}/{dtempfns[0]}'
    dst = f'{data_path}/{year}/Cedolini_{year}_{month:02}.pdf'
    LOGGER.info("mv'ing '%s' to '%s'", src, dst)
    move(src, dst)


def get_last_local(data_path: str) -> Date:
    data_path_p = Path(data_path)

    max_year = max(fn for fn in data_path_p.iterdir() if '.' not in fn.name)
    last_pdf = max(fn for fn in max_year.iterdir() if fn.suffix == '.pdf')
    year, month = map(int, last_pdf.stem.split('_', 2)[1:])
    return Date(year, month)


def try_fetch_new_data(username: str, password: str, data_path: str) -> None:  # noqa: C901
    with (
        TemporaryDirectory() as dtemp,
        Firefox(
            service=Service(executable_path=str(GECKODRIVER_PATH)),
            options=options(dtemp),
        ) as d
    ):  # fmt: skip
        wait = WebDriverWait(d, 30)
        action = ActionChains(d)

        # do login
        d.get('https://login.myareaf2a.com/login/user')
        d.find_element(By.ID, 'username').send_keys(username)
        d.find_element(By.ID, 'password').send_keys(password + Keys.RETURN)
        wait.until(url_contains('home/card/DATI_PERSONALI'))
        # go to "DOCUMENTI PERSONALI"
        d.get('https://www.myareaf2a.com/home/documents/personal')
        wait.until(presence_of_element_located((By.TAG_NAME, 'mat-row')))

        def change_year(year: int) -> int:
            # open year dropdown
            d.find_element(By.CSS_SELECTOR, '.mat-mdc-select-trigger').click()
            # select year
            for mat_option in d.find_elements(
                By.CSS_SELECTOR, '#mat-select-0-panel mat-option'
            ):
                if mat_option.get_attribute('textContent') == f' {year} ':
                    mat_option.click()
                    sleep(1)
                    return year

            raise ValueError

        def download_for_month(year: int, month: int) -> None:
            text = f'{month:02d}/{year:04d}'
            for row in d.find_elements(By.CSS_SELECTOR, '.mat-mdc-row'):
                mese = row.find_element(By.CSS_SELECTOR, '.cdk-column-label')
                if not mese or not mese.get_attribute('textContent').endswith(
                    text
                ):
                    continue
                button = row.find_element(
                    By.CSS_SELECTOR, '.cdk-column-download button'
                )
                d.execute_script(
                    'arguments[0].scrollIntoView({block: "center"})', button
                )
                action.move_to_element(button).perform()
                button.click()
                wait_download(dtemp)
                return
            raise ValueError

        previous_year = datetime.now(tz=UTC).year
        for year, month in get_last_local(data_path).get_year_months():
            if year != previous_year:
                try:
                    previous_year = change_year(year)
                except ValueError:
                    break

            try:
                download_for_month(year, month)
            except ValueError:
                break
            else:
                mv_pdf_from_tmp_to_data(dtemp, year, month, data_path)
