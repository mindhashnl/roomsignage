import os
from asyncio import sleep
from datetime import date, time

from django.conf import settings
import pytest
import chromedriver_binary
from selenium import webdriver
from pytest import mark

# @pytest.fixture(scope="module")
# def driver():
#     driver = webdriver.Chrome()
#     yield driver


def test_index(selenium, live_server):
    print(live_server.url)
    selenium.get(live_server.url)
    assert selenium.title == "MySign"


def test_get_login(selenium, live_server):
    selenium.get(live_server.url + "/login/")
    expected = "MySign"
    assert selenium.title == expected


@mark.django_db
def test_login_admin(selenium, live_server):
    selenium.get(live_server.url + "/login/")
    assert selenium.title == "MySign"

    user = "HMO@utsign.nl"
    pw = "123456"

    user_field = selenium.find_element_by_id("id_username")
    user_field.send_keys(user)

    password_field = selenium.find_element_by_id("id_password")
    password_field.send_keys(pw)

    login_btn = selenium.find_element_by_name("submit")
    login_btn.click()

    assert selenium.current_url == live_server.url + "/admin/door_devices/"


def test_logout_HMO(selenium, live_server):
    selenium.get(live_server.url + "/admin/door_devices")

    logout_btn = selenium.find_element_by_id("logout")
    logout_btn.click()

    assert selenium.current_url == live_server.url + "/admin/door_devices/"
