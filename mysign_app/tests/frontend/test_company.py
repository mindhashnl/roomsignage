from pytest import fixture

from mysign_app.models import Company
from mysign_app.tests.factories import CompanyFactory
from mysign_app.tests.frontend.helpers import authenticate_selenium


@fixture(autouse=True)
def setup_test(selenium, live_server):
    company = CompanyFactory(name="Mindhash", email="info@mindhash.com")

    authenticate_selenium(selenium, live_server, company=company)
    selenium.maximize_window()
    selenium.get(live_server.url + "/company/")


def test_form_is_filled(selenium, live_server):
    company = Company.objects.first()

    assert selenium.find_element_by_id('id_name').get_attribute('value') == company.name
    assert selenium.find_element_by_id('id_email').get_attribute('value') == company.email
    assert selenium.find_element_by_id('id_phone_number').get_attribute('value') == company.phone_number
    assert selenium.find_element_by_id('id_color').get_attribute('value') == company.color[1:].upper()
    assert selenium.find_element_by_id('id_text_color').get_attribute('value') == company.text_color[1:].upper()
    assert selenium.find_element_by_xpath('//div[@id="div_id_logo"]/div/a').get_attribute(
        'href') == live_server + company.logo.url
    assert selenium.find_element_by_xpath('//div[@id="div_id_image"]/div/a').get_attribute(
        'href') == live_server + company.image.url


def set_info(selector, info):
    selector.clear()
    selector.send_keys(info)


def test_live_reload(selenium, live_server):
    # Test clearing image
    selenium.find_element_by_id('image-clear_id').click()
    assert selenium.find_element_by_id('screen_display_image').get_attribute(
        'src') == live_server + '/static/mysign_app/image-fallback.png'
    selenium.find_element_by_id('logo-clear_id').click()
    assert selenium.find_element_by_id('screen_display_logo').get_attribute(
        'src') == live_server + '/static/mysign_app/logo-fallback.png'

    # Test field updating
    set_info(selenium.find_element_by_id('id_email'), '123456')
    assert selenium.find_element_by_id('screen_display_email').text == '123456'
    set_info(selenium.find_element_by_id('id_phone_number'), '123456')
    assert selenium.find_element_by_id('screen_display_phone_number').text == '123456'
    set_info(selenium.find_element_by_id('id_website'), '123456')
    assert selenium.find_element_by_id('screen_display_website').text == '123456'

    # Test color updating
    selenium.find_element_by_id('id_color').clear()
    selenium.find_element_by_id('id_color').send_keys('FFFFFF')
    selenium.find_element_by_id('id_name').click()
    assert selenium.find_element_by_id('screen_display_info').get_attribute(
        'style') == 'background: rgb(255, 255, 255);'

    selenium.find_element_by_id('id_text_color').clear()
    selenium.find_element_by_id('id_text_color').send_keys('000000')
    selenium.find_element_by_id('id_name').click()
    assert selenium.find_element_by_id('screen_display_text').get_attribute('style') == 'color: rgb(0, 0, 0);'


def test_save(selenium):
    set_info(selenium.find_element_by_id('id_name'), 'Example')
    set_info(selenium.find_element_by_id('id_phone_number'), '+3112345678')
    set_info(selenium.find_element_by_id('id_email'), 'info@example.com')
    set_info(selenium.find_element_by_id('id_website'), 'example.com')
    set_info(selenium.find_element_by_id('id_color'), 'FFFFFF')
    set_info(selenium.find_element_by_id('id_text_color'), '000000')
    selenium.find_element_by_id('image-clear_id').click()
    selenium.find_element_by_id('logo-clear_id').click()

    selenium.find_element_by_id('submitButton').click()

    company = Company.objects.first()
    assert company.name == 'Example'
    assert company.phone_number == '+3112345678'
    assert company.email == 'info@example.com'
    assert company.website == 'example.com'
    assert company.color == '#FFFFFF'
    assert company.text_color == '#000000'


def test_save_invalid(selenium):
    set_info(selenium.find_element_by_id('id_phone_number'), '1234')
    selenium.find_element_by_id('submitButton').click()

    assert selenium.find_element_by_id('error_1_id_phone_number')
