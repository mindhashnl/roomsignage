import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from ..factories import CompanyFactory
from ...models import Company


@mark.django_db
def test_create():
    company = CompanyFactory()
    company.full_clean()
    assert Company.objects.count() == 1
    assert Company.objects.first().name == company.name


@mark.django_db
def test_phone_number():
    company = CompanyFactory(phone_number='belmij!')

    with pytest.raises(ValidationError):
        assert not company.full_clean()
