from __future__ import annotations

from datetime import date
from os import listdir
from os import makedirs
from shutil import move
from tempfile import TemporaryDirectory
from typing import Iterable
from typing import NamedTuple

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located)
from selenium.webdriver.support.expected_conditions import url_contains
from selenium.webdriver.support.wait import WebDriverWait

from .constants import GECKODRIVER_PATH


class Date(NamedTuple):
    year: int
    month: int

    def next(self) -> Date:
        if self.month == 11:    # (year, 13) is extra month's salary
            return Date(self.year, 13)
        if self.month == 13:    # (year, 13) happens before (year, 12)
            return Date(self.year, 12)
        if self.month == 12:
            return Date(self.year + 1, 1)
        return Date(self.year, self.month + 1)

    def get_year_months(self) -> Iterable[Date]:
        'infinite generator of (year, month) from last'

        d = self
        while True:
            d = d.next()
            yield d


def firefox_profile(dtemp: str) -> FirefoxProfile:
    profile = FirefoxProfile()

    # disable Firefox's built-in PDF viewer
    profile.set_preference('pdfjs.disabled', True)

    # set download folder
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', dtemp)
    profile.set_preference('browser.helperApps.neverAsk.saveToDisk',
                           'application/octet-stream')

    return profile


def mv_pdf_from_tmp_to_data(dtemp: str, year: int, month: int,
                            data_path: str) -> None:
    makedirs(f'{data_path}/{year}', exist_ok=True)
    move(f'{dtemp}/{listdir(dtemp)[0]}',
         f'{data_path}/{year}/Cedolini_{year}_{month:02}.pdf')


def get_last_local(data_path: str) -> Date:
    max_year = max(fn for fn in listdir(data_path) if '.' not in fn)
    last_pdf = max(fn for fn in listdir(f'{data_path}/{max_year}')
                   if fn.endswith('.pdf'))
    year, month = map(int, last_pdf.split('.', 1)[0].split('_', 2)[1:])
    return Date(year, month)


def try_fetch_new_data(username: str, password: str, data_path: str) -> None:
    with TemporaryDirectory() as dtemp, \
            webdriver.Firefox(executable_path=GECKODRIVER_PATH,
                              firefox_profile=firefox_profile(dtemp)) as d:
        wait = WebDriverWait(d, 10)

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
            d.find_element(By.CSS_SELECTOR,
                           '.mat-form-field-type-mat-select').click()
            # select year
            for mat_option in d.find_elements(By.CSS_SELECTOR,
                                              '.mat-select-panel mat-option'):
                if mat_option.text == str(year):
                    mat_option.click()
                    return year

            raise ValueError()

        def download_for_month(month: int) -> None:
            text = f'{month:02d}'
            for row in d.find_elements(By.TAG_NAME, 'mat-row'):
                mese = row.find_element(By.CSS_SELECTOR, '.cdk-column-mese')
                if not mese or mese.text != text:
                    continue
                row.find_element(By.CSS_SELECTOR,
                                 '.cdk-column-download button').click()
                return
            raise ValueError()

        previous_year = date.today().year
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
