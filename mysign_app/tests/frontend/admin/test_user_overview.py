from selenium.webdriver.common.keys import Keys

from mysign_app.models import Company, User
from mysign_app.tests.frontend.admin.helpers import authenticate_selenium


def user_setup(selenium, live_server):
    Company.objects.create(name="Mindhash", email="info@mindhash.com")
    Company.objects.create(name="Test", email="test@test.com")
    User.objects.create(first_name="Lasse", last_name="Licht", email="lasse@mindhash.nl", is_admin=False)
    User.objects.create(first_name="Jan", last_name="Janssen", email="jan@janssen.nl", is_admin=True)

    authenticate_selenium(selenium, live_server, is_admin=True, first_name="admin")
    selenium.maximize_window()
    selenium.get(live_server.url + "/admin/users/")


def test_card_selected(selenium, live_server):
    user_setup(selenium, live_server)
    card_1 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Lasse Licht']")
    card_2 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Jan Janssen']")

    card_1_parent = card_1.find_element_by_xpath('..')
    card_2_parent = card_2.find_element_by_xpath('..')

    assert "selected" not in card_1_parent.get_attribute("class")
    assert "selected" not in card_2_parent.get_attribute("class")

    card_1.click()
    assert "selected" in card_1_parent.get_attribute("class")
    assert "selected" not in card_2_parent.get_attribute("class")

    card_2.click()
    assert "selected" not in card_1_parent.get_attribute("class")
    assert "selected" in card_2_parent.get_attribute("class")


def test_card_form_data(selenium, live_server):
    user_setup(selenium, live_server)
    card_1 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Lasse Licht']")
    card_2 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Jan Janssen']")

    # first name
    assert "" == selenium.find_element_by_id('id_first_name').get_attribute('value')
    # last name
    assert "" == selenium.find_element_by_id('id_last_name').get_attribute('value')
    # email
    assert "" == selenium.find_element_by_id('id_email').get_attribute('value')
    # company
    assert "" == selenium.find_element_by_id('id_company').get_attribute('value')

    card_1.click()
    assert 'Lasse' == selenium.find_element_by_id('id_first_name').get_attribute('value')
    assert 'Licht' == selenium.find_element_by_id('id_last_name').get_attribute('value')
    assert 'lasse@mindhash.nl' == selenium.find_element_by_id('id_email').get_attribute('value')
    assert '' == selenium.find_element_by_id('id_company').get_attribute('value')
    assert not selenium.find_element_by_id('id_is_admin').is_selected()

    card_2.click()
    assert 'Jan' == selenium.find_element_by_id('id_first_name').get_attribute('value')
    assert 'Janssen' == selenium.find_element_by_id('id_last_name').get_attribute('value')
    assert 'jan@janssen.nl' == selenium.find_element_by_id('id_email').get_attribute('value')
    assert '' == selenium.find_element_by_id('id_company').get_attribute('value')
    assert selenium.find_element_by_id('id_is_admin').is_selected()


def test_disabled_if_none_selected(selenium, live_server):
    user_setup(selenium, live_server)
    assert not selenium.find_element_by_id('id_company').is_enabled()
    assert not selenium.find_element_by_id('id_first_name').is_enabled()
    assert not selenium.find_element_by_id('id_last_name').is_enabled()
    assert not selenium.find_element_by_id('id_is_admin').is_enabled()

    assert not selenium.find_element_by_id('submitButton').is_enabled()
    # assert not selenium.find_element_by_id('deleteButton').is_enabled()

    selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Lasse Licht']").click()
    assert selenium.find_element_by_id('id_company').is_enabled()
    assert selenium.find_element_by_id('id_first_name').is_enabled()
    assert selenium.find_element_by_id('id_last_name').is_enabled()
    assert selenium.find_element_by_id('id_is_admin').is_enabled()

    assert selenium.find_element_by_id('submitButton').is_enabled()
    # assert selenium.find_element_by_id('deleteButton').is_enabled()


def test_save_button(selenium, live_server):
    user_setup(selenium, live_server)

    card = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Lasse Licht']")
    card_parent = card.find_element_by_xpath('..')

    # check if card has no company data
    card.click()
    assert '' == card_parent.find_element_by_xpath("//td[@class='company.name']").text

    # select a new company
    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Mindhash']").click()

    selenium.find_element_by_id('id_first_name').clear()
    selenium.find_element_by_id('id_first_name').send_keys("Las")

    selenium.find_element_by_id('id_last_name').clear()
    selenium.find_element_by_id('id_last_name').send_keys("Ligt")

    selenium.find_element_by_id('id_email').clear()
    selenium.find_element_by_id('id_email').send_keys("las@mindhash.nl")

    # check if save reminder shows up
    assert "You have unsaved changes, please dont forget to save" == selenium.find_element_by_id('collapseDiv').text

    # save
    selenium.find_element_by_id('submitButton').click()

    # reload cards
    card = selenium.find_element_by_xpath("//td[@class='name active sorting_1' and text()='Las Ligt']")
    card_parent = card.find_element_by_xpath('..')
    card.click()
    # check if card now does have company data
    assert 'Mindhash' == card_parent.find_element_by_xpath("//td[@class='company.name active']").text
    assert 'Las Ligt' == card.text
    assert 'las@mindhash.nl' == selenium.find_element_by_id('id_email').get_attribute('value')


def test_search(selenium, live_server):
    user_setup(selenium, live_server)

    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 3

    search = selenium.find_element_by_xpath("//input[@class='form-control w-100']")
    search.send_keys("Las")

    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 1

    search.clear()
    search.send_keys("Jan")
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 1

    search.clear()
    search.send_keys("MySign")
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 0

    search.clear()
    search.send_keys(Keys.ENTER)

    # link company
    card = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Lasse Licht']")
    card.click()
    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Mindhash']").click()
    selenium.find_element_by_id('submitButton').click()

    # search for company
    search = selenium.find_element_by_xpath("//input[@class='form-control w-100']")
    search.send_keys("Mind")
    cards_not_active = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    cards_active = selenium.find_elements_by_xpath("//td[@class='name active sorting_1']")
    assert len(cards_not_active) + len(cards_active) == 1
