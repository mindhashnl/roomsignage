import os
from asyncio import sleep
from datetime import date, time

from django.conf import settings
import pytest
import chromedriver_binary
from selenium import webdriver
from pytest import mark
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import wait

DEFAULT_ENGINE = 'django.db.backends.sqlite3'

HOMEPAGE = 'http://localhost:8000/'
TODAY = date.today()

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver

@pytest.fixture(scope='session')
def test_django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': os.environ.get("DB_ENGINE", DEFAULT_ENGINE),
        'HOST': os.environ["DB_HOST"],
        'NAME': 'MySign.db',  # my dedicated test database (!)
    }

def test_loggedout_homepage(driver):
    driver.get(HOMEPAGE)
    expected = "MySign"
    assert driver.title == expected

def test_get_loginpage(driver):
    driver.get(HOMEPAGE + "login/")
    expected = "MySign"
    assert driver.title == expected

@mark.django_db
def test_login_HMO(driver):
    driver.get(HOMEPAGE + "login/")
    expected = "MySign"
    assert driver.title == expected

    user = "HMO@utsign.nl"
    pw = "123456"

    user_field = driver.find_element_by_id("id_username")
    user_field.send_keys(user)

    password_field = driver.find_element_by_id("id_password")
    password_field.send_keys(pw)

    login_btn = driver.find_element_by_name("submit")
    login_btn.click()

    time.sleep(1000000)

    expected_url = HOMEPAGE + "/admin/door_devices/"
    current_url = driver.current_url
    assert expected_url == current_url



