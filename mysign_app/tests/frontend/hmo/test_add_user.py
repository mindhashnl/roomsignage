from mysign_app.models import Company
from mysign_app.tests.frontend.hmo.helpers import authenticate_selenium


def setup_user_test(selenium, live_server):
    Company.objects.create(name="Mindhash", email="info@mindhash.com")
    Company.objects.create(name="Test", email="test@test.com")

    authenticate_selenium(selenium, live_server, is_admin=True, first_name="admin")
    selenium.maximize_window()
    selenium.get(live_server.url + "/admin/users/add")


def fill_form(selenium, live_server):
    selenium.find_element_by_id('id_user-first_name').send_keys("Test")
    selenium.find_element_by_id('id_user-last_name').send_keys("One")
    selenium.find_element_by_id('id_user-email').send_keys("test@one.com")
    selenium.find_element_by_xpath("// select[ @ id = 'id_user-company'] / option[text() = 'Mindhash']").click()
    selenium.find_element_by_id('id_user-is_admin').click()


# tests if the form is clear when page is loaded
def test_form_clear(selenium, live_server):
    setup_user_test(selenium, live_server)

    assert selenium.find_element_by_id('id_user-first_name').get_attribute('value') == ''
    assert selenium.find_element_by_id('id_user-last_name').get_attribute('value') == ''
    assert selenium.find_element_by_id('id_user-email').get_attribute('value') == ''
    assert selenium.find_element_by_id('id_user-company').get_attribute('value') == ''
    assert not selenium.find_element_by_id('id_user-is_admin').is_selected()


# tests save button and adding of user
def test_save(selenium, live_server):
    setup_user_test(selenium, live_server)
    selenium.get(live_server.url + "/admin/users")

    # starting amount of user cards
    cards_not_active = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    cards_active = selenium.find_elements_by_xpath("//td[@class='name active sorting_1']")
    assert len(cards_not_active) + len(cards_active) == 1

    selenium.get(live_server.url + "/admin/users/add")
    fill_form(selenium, live_server)
    # deselect is_admin
    selenium.find_element_by_id('id_user-is_admin').click()
    # click submit
    selenium.find_element_by_id('submit_button').click()
    # user should be added successfully, so redirect to user page is expected
    assert selenium.current_url == live_server.url + "/admin/users/"

    # since a user has been added, a card should also have been added
    cards_not_active = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    cards_active = selenium.find_elements_by_xpath("//td[@class='name active sorting_1']")
    assert len(cards_not_active) + len(cards_active) == 2


# tests if a user can be added without email
def test_save_no_email(selenium, live_server):
    setup_user_test(selenium, live_server)
    fill_form(selenium, live_server)
    selenium.find_element_by_id('id_user-email').clear()

    selenium.find_element_by_id('submit_button').click()
    # this should be denied, so the current page should still be the add user page
    assert selenium.current_url == live_server.url + "/admin/users/add"


# tests if a user can be added with both a company and as admin
def test_save_company_admin(selenium, live_server):
    setup_user_test(selenium, live_server)
    fill_form(selenium, live_server)

    selenium.find_element_by_id('submit_button').click()
    # this should be denied, so the current page should still be the add user page
    assert selenium.current_url == live_server.url + "/admin/users/add"


# Tests if a user can be added with only is_admin
def test_save_no_company_admin(selenium, live_server):
    setup_user_test(selenium, live_server)
    fill_form(selenium, live_server)

    selenium.find_element_by_xpath("// select[ @ id = 'id_user-company'] / option[text() = '---------']").click()
    selenium.find_element_by_id('submit_button').click()
    assert selenium.current_url == live_server.url + "/admin/users/"


# Tests if a user can be saved with only company selected and not admin
def test_save_company_no_admin(selenium, live_server):
    setup_user_test(selenium, live_server)
    fill_form(selenium, live_server)

    selenium.find_element_by_id('id_user-is_admin').click()
    selenium.find_element_by_id('submit_button').click()
    assert selenium.current_url == live_server.url + "/admin/users/"


# tests cancel button
def test_cancel(selenium, live_server):
    setup_user_test(selenium, live_server)
    selenium.get(live_server.url + "/admin/users")

    # starting amount of cards
    cards_not_active = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    cards_active = selenium.find_elements_by_xpath("//td[@class='name active sorting_1']")
    assert len(cards_not_active) + len(cards_active) == 1

    selenium.get(live_server.url + "/admin/users/add")
    fill_form(selenium, live_server)

    # click cancel
    selenium.find_element_by_id('cancel_button').click()
    # adding should be cancelled, so redirect to user page is expected
    assert selenium.current_url == live_server.url + "/admin/users/"

    # since no user should have been added, the amouont of cards should still be one
    cards_not_active = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    cards_active = selenium.find_elements_by_xpath("//td[@class='name active sorting_1']")
    assert len(cards_not_active) + len(cards_active) == 1
