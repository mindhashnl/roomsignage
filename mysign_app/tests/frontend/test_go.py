from pytest import mark
from mysign_app.tests.frontend.helpers import authenticate_selenium


def test_index(selenium, live_server):
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


def test_logout_HMO(selenium, live_server, client):
    authenticate_selenium(selenium, live_server, is_admin=True)

    selenium.get(live_server.url + "/admin/door_devices")

    assert selenium.current_url == live_server.url + '/admin/door_devices/'

    logout_btn = selenium.find_element_by_id("logout")
    logout_btn.click()

    assert selenium.current_url == live_server.url + "/login/"


def test_navbar_companies(selenium, live_server):
    btn = selenium.find_element_by_id("Companies")
    btn.click()

    assert selenium.current_url == live_server.url + "/admin/companies/"


def test_navbar_devices(selenium, live_server):
    btn = selenium.find_element_by_id("Devices")
    btn.click()

    assert selenium.current_url == live_server.url + "/admin/device_overview/"


def test_navbar_users(selenium, live_server):
    btn = selenium.find_element_by_id("Users")
    btn.click()

    assert selenium.current_url == live_server.url + "/admin/users/"
