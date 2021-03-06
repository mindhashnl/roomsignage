import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from mysign_app.models import User
from mysign_app.tests.factories import CompanyFactory, UserFactory


@mark.django_db
def test_admin_create():
    UserFactory(is_admin=True)
    assert User.objects.count() == 1
    assert User.objects.first().is_admin


@mark.django_db
def test_email_case_insensitive():
    UserFactory(is_admin=True, email='info@example.com')
    user = UserFactory.build(is_admin=True, email='INFO@example.com')

    with pytest.raises(ValidationError):
        user.save()


@mark.django_db
def test_company_create():
    company = CompanyFactory()
    UserFactory(company=company)

    assert User.objects.count() == 1
    assert User.objects.first().company_id == company.id


@mark.django_db
def test_company_and_admin():
    company = CompanyFactory()
    user = UserFactory.build(company=company, is_admin=True)

    with pytest.raises(ValidationError):
        user.save()


@mark.django_db
def test_email_required():
    user = UserFactory.build(email=None, is_admin=True)
    with pytest.raises(ValidationError):
        user.save()


def test_class_name():
    assert User.class_name() == 'User'
