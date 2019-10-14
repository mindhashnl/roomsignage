import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from mysign_app.models import Company, logo_upload
from mysign_app.tests.factories import CompanyFactory, DoorDeviceFactory


@mark.django_db
def test_create():
    company = CompanyFactory()
    company.full_clean()
    assert Company.objects.count() == 1
    assert Company.objects.first().name == company.name


def test_phone_number():
    company = CompanyFactory.build(phone_number='belmij!')

    with pytest.raises(ValidationError):
        company.full_clean()


def test_website():
    company = CompanyFactory.build(website='no-site')

    with pytest.raises(ValidationError):
        company.full_clean()

    company = CompanyFactory.build(website='http://example.com')
    company.full_clean()

    company = CompanyFactory.build(website='example.com')
    company.full_clean()


def test_str():
    company = CompanyFactory.build(name="test")

    assert str(company) == "test"


def test_logo_upload_helper():
    path = logo_upload(None, 'file.png')

    assert path.endswith('.png')
    assert path.startswith('companies/logos/')


def test_logo_fallback():
    company = CompanyFactory.build()

    assert company.logo
    assert company.logo_url_or_default() == company.logo.url

    company = CompanyFactory.build(logo=None)

    assert not company.logo
    assert company.logo_url_or_default() == '/static/mysign_app/logo-fallback.png'


def test_class_name():
    assert Company.class_name() == 'Company'


@mark.django_db
def test_door_devices():
    company = CompanyFactory()

    assert company.door_devices.count() == 0

    door_device = DoorDeviceFactory.build()
    door_device.company = company
    door_device.save()

    assert company.door_devices.count() == 1
    assert company.door_devices.first() == door_device
