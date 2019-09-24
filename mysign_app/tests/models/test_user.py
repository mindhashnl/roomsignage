import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from mysign_app.tests.factories import CompanyFactory, UserFactory
from mysign_app.models import Company, logo_upload, User


@mark.django_db
def test_admin_create():
    user = UserFactory(is_admin=True)
    assert User.objects.count() == 1
    assert User.objects.first().is_admin == True


@mark.django_db
def test_company_create():
    company = CompanyFactory()
    user = UserFactory(company=company)

    assert User.objects.count() == 1
    assert User.objects.first().company_id == company.id


@mark.django_db
def test_company_and_admin():
    company = CompanyFactory()
    user = UserFactory.build(company=company, is_admin=True)

    with pytest.raises(ValidationError):
        user.save()


@mark.django_db
def test_empty():
    user = UserFactory.build(company=None, is_admin=False)

    with pytest.raises(ValidationError):
        user.save()
