import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from mysign_app.models import Company, logo_upload
from mysign_app.tests.factories import CompanyFactory


@mark.django_db
def test_create():
    company = CompanyFactory()
    company.full_clean()
    assert Company.objects.count() == 1
    assert Company.objects.first().name == company.name


def test_phone_number():
    company = CompanyFactory.build(phone_number='belmij!')

    with pytest.raises(ValidationError):
        assert not company.full_clean()


def test_str():
    company = CompanyFactory.build(name="test")

    assert str(company) == "test"


def test_logo_upload_helper():
    path = logo_upload(None, 'file.png')

    assert path.endswith('.png')
    assert path.startswith('companies/logos/')
