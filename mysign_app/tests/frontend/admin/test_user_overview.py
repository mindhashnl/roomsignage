from pytest import fixture
from selenium.webdriver.common.keys import Keys

from mysign_app.models import Company, User
from mysign_app.tests.frontend.helpers import authenticate_selenium


@fixture(autouse=True)
def user_setup(selenium, live_server):
    Company.objects.create(name="Mindhash", email="info@mindhash.com")
    Company.objects.create(name="Test", email="test@test.com")
    User.objects.create(first_name="John", last_name="Doe", email="john@doe.nl", is_admin=False)
    User.objects.create(first_name="Jan", last_name="Janssen", email="jan@janssen.nl", is_admin=True)

    authenticate_selenium(selenium, live_server, is_admin=True, first_name="admin")
    selenium.maximize_window()
    selenium.get(live_server.url + "/admin/users/")


def test_card_selected(selenium):
    card_1 = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")[0]
    card_2 = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")[1]

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


def test_card_form_data(selenium):
    # checks if form data is empty when no card is selected
    # first name
    assert "" == selenium.find_element_by_id('id_first_name').get_attribute('value')
    # last name
    assert "" == selenium.find_element_by_id('id_last_name').get_attribute('value')
    # email
    assert "" == selenium.find_element_by_id('id_email').get_attribute('value')
    # company
    assert "" == selenium.find_element_by_id('id_company').get_attribute('value')

    # checks if form data is filled correctly
    assert len(selenium.find_elements_by_xpath("//td[@class='name sorting_1']")) == 3

    selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='John Doe']").click()
    assert 'John' == selenium.find_element_by_id('id_first_name').get_attribute('value')
    assert 'Doe' == selenium.find_element_by_id('id_last_name').get_attribute('value')
    assert 'john@doe.nl' == selenium.find_element_by_id('id_email').get_attribute('value')
    assert '' == selenium.find_element_by_id('id_company').get_attribute('value')
    assert not selenium.find_element_by_id('id_is_admin').is_selected()

    selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Jan Janssen']").click()
    assert 'Jan' == selenium.find_element_by_id('id_first_name').get_attribute('value')
    assert 'Janssen' == selenium.find_element_by_id('id_last_name').get_attribute('value')
    assert 'jan@janssen.nl' == selenium.find_element_by_id('id_email').get_attribute('value')
    assert '' == selenium.find_element_by_id('id_company').get_attribute('value')
    assert selenium.find_element_by_id('id_is_admin').is_selected()

    # checks if form data is empty when card is deselected
    selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Jan Janssen']").click()
    # first name
    assert "" == selenium.find_element_by_id('id_first_name').get_attribute('value')
    # last name
    assert "" == selenium.find_element_by_id('id_last_name').get_attribute('value')
    # email
    assert "" == selenium.find_element_by_id('id_email').get_attribute('value')
    # company
    assert "" == selenium.find_element_by_id('id_company').get_attribute('value')


def test_disabled_if_none_selected(selenium):
    assert not selenium.find_element_by_id('id_company').is_enabled()
    assert not selenium.find_element_by_id('id_first_name').is_enabled()
    assert not selenium.find_element_by_id('id_last_name').is_enabled()
    assert not selenium.find_element_by_id('id_is_admin').is_enabled()

    assert not selenium.find_element_by_id('submitButton').is_enabled()

    selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='John Doe']").click()
    assert selenium.find_element_by_id('id_company').is_enabled()
    assert selenium.find_element_by_id('id_first_name').is_enabled()
    assert selenium.find_element_by_id('id_last_name').is_enabled()
    assert selenium.find_element_by_id('id_is_admin').is_enabled()

    assert selenium.find_element_by_id('submitButton').is_enabled()


def test_save_button(selenium):
    card = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='John Doe']")
    card_parent = card.find_element_by_xpath('..')

    # check if card has no company data
    card.click()
    assert '' == card_parent.find_element_by_xpath("//td[@class='company.name']").text

    # select a new company
    assert not selenium.find_element_by_id('collapseDiv').is_displayed()
    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Mindhash']").click()

    selenium.find_element_by_id('id_first_name').clear()
    selenium.find_element_by_id('id_first_name').send_keys("Las")

    selenium.find_element_by_id('id_last_name').clear()
    selenium.find_element_by_id('id_last_name').send_keys("Ligt")

    selenium.find_element_by_id('id_email').clear()
    selenium.find_element_by_id('id_email').send_keys("las@mindhash.nl")

    # check if save reminder shows up
    assert selenium.find_element_by_id('collapseDiv').is_displayed()

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


def test_invalid_save(selenium):
    card = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Jan Janssen']")
    card.click()

    # Make form invalid (by setting admin and company)
    assert selenium.find_element_by_id('id_is_admin').is_selected()
    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Mindhash']").click()
    selenium.find_element_by_id('submitButton').click()

    # Check that there is a error in the form
    error_card = selenium.find_element_by_xpath("//div[@class='alert alert-block alert-danger']")
    assert error_card
    assert error_card.text == 'Company and is_admin cannot set both'


def test_remove_button(selenium):
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    # check that the total amount of cards is 2
    assert len(cards) == 3

    # select the card and press delete
    cards[0].click()
    selenium.find_element_by_id("deleteButton").click()

    # check chrome popup, click "Cancel"
    selenium.switch_to.alert.dismiss()
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 3

    selenium.find_element_by_id("deleteButton").click()

    # check chrome popup, click Accept"
    selenium.switch_to.alert.accept()
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 2


def test_search(selenium):
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 3

    search = selenium.find_element_by_xpath("//input[@class='form-control w-100']")
    search.send_keys("John")

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
    card = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")[1]
    card.click()

    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Mindhash']").click()
    if selenium.find_element_by_id('id_is_admin').is_selected():
        selenium.find_element_by_id('id_is_admin').click()
    selenium.find_element_by_id('submitButton').click()
    # search for company
    search = selenium.find_element_by_xpath("//input[@class='form-control w-100']")
    search.send_keys("Mind")
    cards_not_active = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    cards_active = selenium.find_elements_by_xpath("//td[@class='name active sorting_1']")
    assert len(cards_not_active) + len(cards_active) == 1
