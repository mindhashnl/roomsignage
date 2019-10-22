from mysign_app.models import Company
from mysign_app.tests.frontend.helpers import authenticate_selenium


def company_setup(selenium, live_server):
    Company.objects.create(name="Test", email="test@test.com")
    Company.objects.create(name="Test_2", email="test_2@test.com")
    authenticate_selenium(selenium, live_server, is_admin=True)
    selenium.maximize_window()
    selenium.get(live_server.url + "/admin/companies/")


def test_card_form_data(selenium, live_server):
    company_setup(selenium, live_server)
    card_1 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Test']")
    card_2 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Test_2']")

    # name
    assert "" == selenium.find_element_by_id('id_name').get_attribute('value')
    # email
    assert "" == selenium.find_element_by_id('id_email').get_attribute('value')

    card_1.click()
    assert 'Test' == selenium.find_element_by_id('id_name').get_attribute('value')
    assert 'test@test.com' == selenium.find_element_by_id('id_email').get_attribute('value')

    card_2.click()
    assert 'Test_2' == selenium.find_element_by_id('id_name').get_attribute('value')
    assert 'test_2@test.com' == selenium.find_element_by_id('id_email').get_attribute('value')


def test_form_fields_disabled(selenium, live_server):
    company_setup(selenium, live_server)
    card_1 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Test']")
    card_1.click()

    name_field = selenium.find_element_by_id('id_name')
    text_name = name_field.get_attribute('value')

    name_field.send_keys("MySign")
    assert text_name == name_field.get_attribute('value')
    assert not text_name == "MySign"

    email_field = selenium.find_element_by_id('id_email')
    text_email = email_field.get_attribute('value')

    email_field.send_keys("MySign")
    assert text_email == email_field.get_attribute('value')
    assert not text_email == "MySign"


def test_card_selected(selenium, live_server):
    company_setup(selenium, live_server)
    card_1 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Test']")
    card_2 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Test_2']")

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


def test_remove_button_disabled(selenium, live_server):
    company_setup(selenium, live_server)

    assert not selenium.find_element_by_id("deleteButton").is_enabled()


def test_remove_button_enabled(selenium, live_server):
    company_setup(selenium, live_server)

    assert not selenium.find_element_by_id("deleteButton").is_enabled()

    selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Test']").click()
    assert selenium.find_element_by_id("deleteButton").is_enabled()


def test_alert_present(selenium, live_server):
    company_setup(selenium, live_server)
    card_1 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Test']")

    card_1.click()
    selenium.find_element_by_id("deleteButton").click()
    # check if alert appears, if you cant switch it does not exist
    assert selenium.switch_to_alert


def test_remove_button(selenium, live_server):
    company_setup(selenium, live_server)
    card_1 = selenium.find_element_by_xpath("//td[@class='name sorting_1' and text()='Test']")

    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 2

    card_1.click()
    selenium.find_element_by_id("deleteButton").click()

    # check chrome popup, click "Cancel"
    selenium.switch_to.alert.dismiss()
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 2

    selenium.find_element_by_id("deleteButton").click()

    # check chrome popup, click Accept"
    selenium.switch_to.alert.accept()
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 1


def test_search(selenium, live_server):
    company_setup(selenium, live_server)

    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 2

    search = selenium.find_element_by_xpath("//input[@class='form-control w-100']")
    search.send_keys("test")

    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 2

    search.clear()
    search.send_keys("test_2")
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 1

    search.send_keys("MySign")
    cards = selenium.find_elements_by_xpath("//td[@class='name sorting_1']")
    assert len(cards) == 0
