from configparser import ConfigParser
from dataclasses import dataclass
from datetime import date
from os import listdir
from shutil import rmtree
from tempfile import mkdtemp
from typing import Iterable
from shutil import move

from PySide6.QtCore import QSettings
from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.firefox.firefox_profile import FirefoxProfile
from selenium.webdriver.support.expected_conditions import \
    element_to_be_clickable
from selenium.webdriver.support.expected_conditions import new_window_is_opened
from selenium.webdriver.support.expected_conditions import \
    presence_of_element_located
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait

from .constants import SETTINGS_DATA_PATH

GECKODRIVER_PATH = 'bin/geckodriver-v0.30.0-win64/geckodriver.exe'
SECRETS_PATH = 'secrets.ini'


@dataclass
class Secrets:
    username: str
    password: str


def get_secrets() -> Secrets:
    config = ConfigParser()
    with open(SECRETS_PATH, encoding='utf-8') as secrets_file:
        config.read_file(secrets_file)
    myareaf2a = config['myareaf2a']
    return Secrets(username=myareaf2a['username'],
                   password=myareaf2a['password'])


def get_year_months(last: date) -> Iterable[tuple[int, int]]:
    'infinite generator of (year, month) from last'

    def next_month(d: date) -> date:
        'add a month - avoid adding a dependency just for this'
        if d.month == 12:
            return date(d.year + 1, 1, 1)
        return date(d.year, d.month + 1, 1)

    d = last
    while True:
        d = next_month(d)
        yield (d.year, d.month)
        if d.month == 12:
            yield (d.year, 13)


def firefox_profile(dtemp: str) -> FirefoxProfile:
    profile = FirefoxProfile()

    # disable Firefox's built-in PDF viewer
    profile.set_preference('pdfjs.disabled', True)

    # set download folder
    profile.set_preference('browser.download.folderList', 2)
    profile.set_preference('browser.download.dir', dtemp)
    profile.set_preference(
        'browser.helperApps.neverAsk.saveToDisk',
        'text/csv,application/pdf,application/csv,application/vnd.ms-excel')

    return profile


def mv_pdf_from_tmp_to_data(dtemp: str,
                            year: int,
                            month: int,
                            settings: QSettings
                            ) -> None:
    data_path = settings.value(SETTINGS_DATA_PATH)
    move(f'{dtemp}/{listdir(dtemp)[0]}',
         f'{data_path}/{year}/Cedolini_{year}_{month:02}.pdf')


def try_fetch_new_data(last: date, settings: QSettings) -> bool:
    secrets = get_secrets()
    dtemp = mkdtemp()
    with webdriver.Firefox(executable_path=GECKODRIVER_PATH,
                           firefox_profile=firefox_profile(dtemp)) as driver:
        wait = WebDriverWait(driver, 10)

        # do login
        driver.get('https://login.myareaf2a.com/login/user')
        driver.find_element(By.ID, 'mat-input-0').send_keys(secrets.username)
        driver.find_element(By.ID, 'mat-input-1').send_keys(secrets.password +
                                                            Keys.RETURN)
        # wait for logged hp
        wait.until(presence_of_element_located(
            (By.TAG_NAME, 'app-header-menu-user-profile')))

        # click on 'Apri tutti i documenti personali'
        driver.find_element(By.CSS_SELECTOR, '.apps-button').click()
        driver.find_element(By.CSS_SELECTOR, '.applicationButton').click()
        if len(driver.window_handles) == 1:
            wait.until(new_window_is_opened(driver.window_handles))
        driver.switch_to.window(driver.window_handles[-1])

        # naviga
        wait.until(element_to_be_clickable((By.CSS_SELECTOR,
                                            '#menudoc'))).click()
        wait.until(element_to_be_clickable((By.CSS_SELECTOR,
                                            '#imgCEDOLINO'))).click()

        whs = {
            'hp': driver.window_handles[0],
            'documenti': driver.window_handles[1],
            'popup': None,
            'pdf': None
        }

        def set_popup_wh() -> None:
            if whs['popup'] in driver.window_handles:
                driver.switch_to.window(whs['popup'])
            else:
                new_whs = driver.window_handles[:]
                new_whs.remove(whs['hp'])
                new_whs.remove(whs['documenti'])
                assert len(new_whs) == 1
                whs['popup'] = new_whs[0]
                driver.switch_to.window(whs['popup'])

        def set_pdf_wh() -> None:
            if whs['pdf'] in driver.window_handles:
                driver.switch_to.window(whs['pdf'])
            else:
                new_whs = driver.window_handles[:]
                new_whs.remove(whs['hp'])
                new_whs.remove(whs['documenti'])
                new_whs.remove(whs['popup'])
                assert len(new_whs) == 1
                whs['pdf'] = new_whs[0]
                driver.switch_to.window(whs['pdf'])

        for (year, month) in get_year_months(last):
            try:
                anno = Select(
                    wait.until(presence_of_element_located((By.ID, 'anno'))))
                mese = Select(
                    wait.until(presence_of_element_located((By.ID, 'mese'))))
                anno.select_by_visible_text(f'{year}')
                mese.select_by_visible_text(f'{month:02}')
                # click on the "pdf" icon on the first column of the results
                wait.until(presence_of_element_located(
                    (By.CSS_SELECTOR,
                     '.ResultRP tr:nth-child(2) div[onclick]'))).click()
            except NoSuchElementException:
                break

            try:
                # a popup is opened
                set_popup_wh()
                # set to download the "original", not the "copy" (?)
                wait.until(element_to_be_clickable(
                    (By.CSS_SELECTOR, '[name=originale][value="1"]')
                )).click()
                # fetch the pdf
                wait.until(element_to_be_clickable(
                    (By.CSS_SELECTOR, '.new_button.ButtonSP')
                )).click()
                # the popup will auto-close, a new one with the .pdf is opened
                set_pdf_wh()
                # now the a pdf should be present in dtemp
                mv_pdf_from_tmp_to_data(dtemp, year, month, settings)
            finally:
                driver.switch_to.window(whs['documenti'])
    rmtree(dtemp)

    return False
