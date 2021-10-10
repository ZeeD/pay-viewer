from dataclasses import dataclass
from configparser import ConfigParser
from datetime import date

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support.expected_conditions import (
    presence_of_element_located, element_to_be_clickable, new_window_is_opened
)
from typing import Generator, Iterable
from selenium.webdriver.support.ui import Select

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
    # TODO
    yield (2021, 9)


def try_fetch_new_data(last: date) -> bool:
    secrets = get_secrets()
    with webdriver.Firefox(executable_path=GECKODRIVER_PATH) as driver:
        wait = WebDriverWait(driver, 10)

        # do loing
        driver.get('https://login.myareaf2a.com/login/user')
        driver.find_element(By.ID, 'mat-input-0').send_keys(secrets.username)
        driver.find_element(By.ID, 'mat-input-1').send_keys(secrets.password +
                                                            Keys.RETURN)
        # wait for logged hp
        wait.until(presence_of_element_located((By.TAG_NAME,
                                                'app-header-menu-user-profile')))

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

        anno = Select(wait.until(presence_of_element_located((By.ID, 'anno'))))
        mese = Select(wait.until(presence_of_element_located((By.ID, 'mese'))))
        for (year, month) in get_year_months(last):
            anno.select_by_visible_text(f'{year}')
            mese.select_by_visible_text(f'{month:02}')
            wait.until(presence_of_element_located(
                (By.CSS_SELECTOR,
                 '.ResultRP tr:nth-child(2) div[onclick]'))).click()

        wait.until(presence_of_element_located((By.TAG_NAME, 'sarcazzo')))

    return False
