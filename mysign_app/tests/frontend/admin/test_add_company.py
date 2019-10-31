from pytest import fixture

from mysign_app.models import Company, User
from mysign_app.tests.frontend.helpers import authenticate_selenium


@fixture(autouse=True)
def setup_test(selenium, live_server):
    Company.objects.create(name="Mindhash", email="info@mindhash.com")
    Company.objects.create(name="Test", email="test@test.com")

    authenticate_selenium(selenium, live_server, is_admin=True, first_name="admin")
    selenium.maximize_window()
    selenium.get(live_server.url + "/admin/companies/add")


# tests if the form is clear when page is loaded
def test_form_clear(selenium):
    assert selenium.find_element_by_id('id_company-name').get_attribute('value') == ''
    assert selenium.find_element_by_id('id_company-email').get_attribute('value') == ''
    assert selenium.find_element_by_id('id_user-first_name').get_attribute('value') == ''
    assert selenium.find_element_by_id('id_user-last_name').get_attribute('value') == ''
    assert selenium.find_element_by_id('id_user-email').get_attribute('value') == ''


def test_save(selenium):
    assert User.objects.count() == 1
    assert Company.objects.count() == 2

    # Fill in form
    selenium.find_element_by_id('id_company-name').send_keys("Company")
    selenium.find_element_by_id('id_company-email').send_keys("info@example.com")
    selenium.find_element_by_id('id_user-first_name').send_keys("First")
    selenium.find_element_by_id('id_user-last_name').send_keys("Last")
    selenium.find_element_by_id('id_user-email').send_keys("user@example.com")
    selenium.find_element_by_id('submit_button').click()

    # Test objects are created
    user = User.objects.filter(first_name='First', last_name='Last', email='user@example.com')
    company = Company.objects.filter(name='Company', email='info@example.com')
    assert user
    assert company
    assert user.first().company == company.first()


def test_cancel(selenium, live_server):
    selenium.find_element_by_id('cancel_button').click()

    assert selenium.current_url == live_server + '/admin/companies/'
