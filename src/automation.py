from __future__ import annotations

from datetime import UTC
from datetime import datetime
from itertools import count
from logging import info
from os import listdir
from pathlib import Path
from shutil import move
from tempfile import TemporaryDirectory
from time import sleep
from typing import TYPE_CHECKING
from typing import Final
from typing import NamedTuple

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver import Firefox
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

from constants import GECKODRIVER_PATH

if TYPE_CHECKING:
    from collections.abc import Iterable


NOV: Final = 11
DIC: Final = 12
TRED: Final = 13


class Date(NamedTuple):
    year: int
    month: int

    def get_year_months(self) -> Iterable[Date]:
        "Infinite generator of (year, month) from last."
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
    options = Options()

    options.profile = FirefoxProfile()

    # disable Firefox's built-in PDF viewer
    options.profile.set_preference('pdfjs.disabled', value=True)

    # set download folder
    options.profile.set_preference('browser.download.folderList', 2)
    options.profile.set_preference('browser.download.dir', dtemp)
    options.profile.set_preference(
        'browser.helperApps.neverAsk.saveToDisk', 'application/octet-stream'
    )

    return options


def wait_download(dtemp: str) -> None:
    info('wait_download (initial: %s)', listdir(dtemp))
    while not listdir(dtemp):
        sleep(0.5)
        info('wait_download [empty]')
    while any(fn.endswith('.part') for fn in listdir(dtemp)):
        sleep(0.5)
        info('wait_download [.part]')


def mv_pdf_from_tmp_to_data(
    dtemp: str, year: int, month: int, data_path: str
) -> None:
    Path(f'{data_path}/{year}').mkdir(parents=True)

    info('files in dtemp:')
    for dtempfn in listdir(dtemp):
        info('\t%s/%s', dtemp, dtempfn)
    src = f'{dtemp}/{listdir(dtemp)[0]}'
    dst = f'{data_path}/{year}/Cedolini_{year}_{month: 02}.pdf'
    info("mv'ing '%s' to '%s'", src, dst)
    move(src, dst)


def get_last_local(data_path: str) -> Date:
    max_year = max(fn for fn in listdir(data_path) if '.' not in fn)
    last_pdf = max(
        fn for fn in listdir(f'{data_path}/{max_year}') if fn.endswith('.pdf')
    )
    year, month = map(int, last_pdf.split('.', 1)[0].split('_', 2)[1:])
    return Date(year, month)


def try_fetch_new_data(username: str, password: str, data_path: str) -> None:  # noqa: C901
    with TemporaryDirectory() as dtemp, Firefox(
        service=Service(executable_path=str(GECKODRIVER_PATH)),
        options=options(dtemp),
    ) as d:
        wait = WebDriverWait(d, 30)

        # do login
        d.get('https://login.myareaf2a.com/login/user')
        d.find_element(By.ID, 'mat-input-0').send_keys(username)
        d.find_element(By.ID, 'mat-input-1').send_keys(password + Keys.RETURN)
        wait.until(url_contains('home/card/DATI_PERSONALI'))
        # go to "DOCUMENTI PERSONALI"
        d.get('https://www.myareaf2a.com/home/documents/personal')
        wait.until(presence_of_element_located((By.TAG_NAME, 'mat-row')))

        def change_year(year: int) -> int:
            # open year dropdown
            d.find_element(
                By.CSS_SELECTOR, '.mat-form-field-type-mat-select'
            ).click()
            # select year
            for mat_option in d.find_elements(
                By.CSS_SELECTOR, '.mat-select-panel mat-option'
            ):
                if mat_option.text == str(year):
                    mat_option.click()
                    return year

            raise ValueError

        def download_for_month(month: int) -> None:
            text = f'{month: 02d}'
            for i in count(2):
                try:
                    row = d.find_element(
                        By.CSS_SELECTOR, f'.mat-row: nth-child({i})'
                    )
                except NoSuchElementException:
                    break
                mese = row.find_element(By.CSS_SELECTOR, '.cdk-column-mese')
                if not mese or mese.text != text:
                    continue
                row.find_element(
                    By.CSS_SELECTOR, '.cdk-column-download button'
                ).click()
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
                download_for_month(month)
            except ValueError:
                break
            else:
                mv_pdf_from_tmp_to_data(dtemp, year, month, data_path)
