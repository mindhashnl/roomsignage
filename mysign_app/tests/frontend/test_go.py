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


def test_index(selenium, live_server):
    selenium.get(live_server.url)
    assert selenium.title == "MySign"


def test_get_login(selenium, live_server):
    selenium.get(live_server.url + "login/")
    expected = "MySign"
    assert selenium.title == expected


@mark.django_db
def test_login_admin(selenium, live_server):
    selenium.get(live_server.url + "login/")
    assert selenium.title == "MySign"

    user = "HMO@utsign.nl"
    pw = "123456"

    user_field = selenium.find_element_by_id("id_username")
    user_field.send_keys(user)

    password_field = selenium.find_element_by_id("id_password")
    password_field.send_keys(pw)

    login_btn = selenium.find_element_by_name("submit")
    login_btn.click()

    time.sleep(1000000)

    assert selenium.current_url == live_server.url + "/admin/door_devices/"
