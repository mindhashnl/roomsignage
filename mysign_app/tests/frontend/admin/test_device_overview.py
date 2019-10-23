from pytest import fixture
from selenium.webdriver.common.keys import Keys

from mysign_app.models import Company, DoorDevice
from mysign_app.tests.frontend.helpers import authenticate_selenium


@fixture(autouse=True)
def device_setup(selenium, live_server):
    Company.objects.create(name="Test", email="test@test.com")
    Company.objects.create(name="Test_2", email="test_2@test.com")

    DoorDevice.objects.create()
    DoorDevice.objects.create()

    authenticate_selenium(selenium, live_server, is_admin=True)
    selenium.maximize_window()
    selenium.get(live_server.url + "/admin/door_devices/")


def test_card_selected(selenium):
    card_1 = selenium.find_element_by_xpath("//td[@class='id sorting_1' and text()='1']")
    card_2 = selenium.find_element_by_xpath("//td[@class='id sorting_1' and text()='2']")

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
    card_1 = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")[0]

    # name
    assert "" == selenium.find_element_by_id('id_company').get_attribute('value')

    # Click card 1, check if no company selected, select company, check if right company selected,
    # Click other company, and check if company changed
    card_1.click()
    assert '' == selenium.find_element_by_id('id_company').get_attribute('value')
    company_id = selenium.find_element_by_xpath(
        "// select[ @ id = 'id_company'] / option[text() = 'Test']").get_attribute(
        'value')
    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Test']").click()
    assert company_id == selenium.find_element_by_id('id_company').get_attribute('value')
    company_id = selenium.find_element_by_xpath(
        "// select[ @ id = 'id_company'] / option[text() = 'Test_2']").get_attribute(
        'value')
    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Test_2']").click()
    assert company_id == selenium.find_element_by_id('id_company').get_attribute('value')


def test_disabled_if_none_selected(selenium):
    assert not selenium.find_element_by_id('id_company').is_enabled()
    assert not selenium.find_element_by_id('submitButton').is_enabled()
    assert not selenium.find_element_by_id('deleteButton').is_enabled()

    selenium.find_element_by_xpath("//td[@class='id sorting_1' and text()='5']").click()
    assert selenium.find_element_by_id('id_company').is_enabled()
    assert selenium.find_element_by_id('submitButton').is_enabled()
    assert selenium.find_element_by_id('deleteButton').is_enabled()


def test_save_door_device(selenium):
    card = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")[0]
    card_parent = card.find_element_by_xpath('..')

    # check if card has no company data
    card.click()
    assert '' == card_parent.find_element_by_xpath("//td[@class='company.name']").text

    # select a new company
    id = selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Test']").get_attribute(
        'value')
    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Test']").click()
    assert id == selenium.find_element_by_id('id_company').get_attribute('value')

    # check if save reminder shows up
    assert "You have unsaved changes, please dont forget to save" == selenium.find_element_by_id('collapseDiv').text

    # save
    selenium.find_element_by_id('submitButton').click()

    # reload cards
    card = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")[0]
    card_parent = card.find_element_by_xpath('..')

    # check if card now does have company data
    assert 'Test' == card_parent.find_element_by_xpath("//td[@class='company.name active']").text


def test_remove_button(selenium):
    card = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")[0]

    cards = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")
    # check that the total amount of cards is 2
    assert len(cards) == 2

    # select the card and press delete
    card.click()
    selenium.find_element_by_id("deleteButton").click()

    # check chrome popup, click "Cancel"
    selenium.switch_to.alert.dismiss()
    cards = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")
    assert len(cards) == 2

    selenium.find_element_by_id("deleteButton").click()

    # check chrome popup, click Accept"
    selenium.switch_to.alert.accept()
    cards = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")
    assert len(cards) == 1


def test_search(selenium):
    # search for cards with id 1, assert that 1 card is visible
    id_1 = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")[0].text
    id_2 = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")[1].text

    search = selenium.find_element_by_xpath("//input[@class='form-control w-100']")
    search.send_keys(id_1)

    cards = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")
    assert len(cards) == 1

    search.clear()
    # search for cards with id 2, assert 1 card is visible
    search.send_keys(id_2)
    cards = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")
    assert len(cards) == 1

    # search for cards with non-existing id
    search.send_keys("-1")
    cards = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")
    assert len(cards) == 0

    # clear search
    search.clear()
    search.send_keys(Keys.ENTER)

    # link company
    card = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")[0]
    card.click()
    selenium.find_element_by_xpath("// select[ @ id = 'id_company'] / option[text() = 'Test']").click()
    selenium.find_element_by_id('submitButton').click()

    # search for company, assert 1 card is found
    search = selenium.find_element_by_xpath("//input[@class='form-control w-100']")
    search.send_keys("Test")
    cards_not_active = selenium.find_elements_by_xpath("//td[@class='id sorting_1']")
    cards_active = selenium.find_elements_by_xpath("//td[@class='id active sorting_1']")
    assert len(cards_not_active) + len(cards_active) == 1
