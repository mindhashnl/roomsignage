import time
from pytest import mark
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from mysign_app.management.commands.seed import Command
from mysign_app.tests.Frontend.hmo.helpers import authenticate_selenium


@mark.django_db
def test_login_admin(selenium, live_server):
    selenium.maximize_window()
    Command().handle()

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


@mark.django_db
def test_logout_HMO(selenium, live_server, client):
    selenium.maximize_window()
    authenticate_selenium(selenium, live_server, is_admin=True)
    selenium.get(live_server.url + "/admin/door_devices")

    assert selenium.current_url == live_server.url + '/admin/door_devices/'

    selenium.find_element_by_id('logout-icon').click()

    assert selenium.current_url == live_server.url + "/login/"


def test_navbar_companies(selenium, live_server):
    selenium.maximize_window()
    authenticate_selenium(selenium, live_server, is_admin=True)
    selenium.get(live_server.url + "/admin/door_devices")

    selenium.find_element_by_id("Companies").click()
    assert selenium.current_url == live_server.url + "/admin/companies/"


def test_navbar_devices(selenium, live_server):
    selenium.maximize_window()
    authenticate_selenium(selenium, live_server, is_admin=True)
    selenium.get(live_server.url + "/admin/door_devices")

    btn = selenium.find_element_by_id("Devices")
    btn.click()

    assert selenium.current_url == live_server.url + "/admin/door_devices/"


def test_navbar_users(selenium, live_server):
    selenium.maximize_window()
    authenticate_selenium(selenium, live_server, is_admin=True)
    selenium.get(live_server.url + "/admin/door_devices")

    selenium.find_element_by_id("Users").click()
    assert selenium.current_url == live_server.url + "/admin/users/"


def test_navbar_add_user(selenium, live_server):
    selenium.maximize_window()
    authenticate_selenium(selenium, live_server, is_admin=True)
    selenium.get(live_server.url + "/admin/users/")

    assert selenium.current_url == live_server.url + "/admin/users/"

    selenium.find_element_by_id('user-add-icon').click()

    assert selenium.current_url == live_server.url + "/admin/users/add"


def test_navbar_add_company(selenium, live_server):
    selenium.maximize_window()
    authenticate_selenium(selenium, live_server, is_admin=True)
    selenium.get(live_server.url + "/admin/companies/")

    assert selenium.current_url == live_server.url + "/admin/companies/"

    selenium.find_element_by_id('company-add-icon').click()

    assert selenium.current_url == live_server.url + "/admin/companies/add/"
