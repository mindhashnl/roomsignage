from django.core import mail
from django.urls import reverse
from pytest import mark

from mysign_app.forms import (AddCompanyUserForm, CompanyForm, DoorDeviceForm,
                              UserForm)
from mysign_app.models import Company, DoorDevice, User
from mysign_app.tests.factories import (CompanyFactory, DoorDeviceFactory,
                                        UserFactory)
from mysign_app.tests.routes.authentication_helpers import (client_login,
                                                            is_admin_route)
from mysign_app.tests.routes.form_helpers import payload_from_form


def test_index(client):
    response = client.get(reverse('admin_index'))

    assert response.status_code == 302
    assert response.url == reverse('admin_door_devices')


@mark.django_db
def test_door_devices(client):
    is_admin_route(client, reverse('admin_door_devices'))


@mark.django_db
def test_companies(client):
    is_admin_route(client, reverse('admin_companies'))


@mark.django_db
def test_company_add(client):
    is_admin_route(client, reverse('admin_company_add'))

    client_login(client, is_admin=True)
    company_payload = payload_from_form(CompanyForm(instance=CompanyFactory.build()), prefix='company')
    user_payload = payload_from_form(AddCompanyUserForm(instance=UserFactory.build()), prefix='user')
    payload = {**company_payload, **user_payload}

    response = client.post(reverse('admin_company_add'), payload)

    assert response.status_code == 302
    assert response.url == reverse('admin_companies')
    assert Company.objects.count() == 1
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Welkom'
    assert User.objects.count() == 2  # One is logged in user, other created user


@mark.django_db
def test_user_add(client):
    is_admin_route(client, reverse('admin_user_add'))

    client_login(client, is_admin=True)
    user_payload = payload_from_form(AddCompanyUserForm(instance=UserFactory.build()), prefix='user')
    payload = {**user_payload}

    response = client.post(reverse('admin_user_add'), payload)

    assert response.status_code == 302
    assert response.url == reverse('admin_users')
    assert len(mail.outbox) == 1
    assert mail.outbox[0].subject == 'Welkom'
    assert User.objects.count() == 2  # One is logged in user, other created user


@mark.django_db
def test_users(client):
    is_admin_route(client, reverse('admin_users'))


@mark.django_db
def test_users_update(client):
    client_login(client, is_admin=True)

    user = UserFactory()

    user.first_name = 'New name'
    payload = payload_from_form(UserForm(instance=user))
    response = client.post(reverse('admin_users'), payload)

    assert response.status_code == 200
    assert User.objects.get(id=user.id).first_name == 'New name'


@mark.django_db
def test_door_device_update(client):
    client_login(client, is_admin=True)

    door_device = DoorDeviceFactory()
    company = CompanyFactory()
    door_device.company = company

    payload = payload_from_form(DoorDeviceForm(instance=door_device))
    response = client.post(reverse('admin_door_devices'), payload)

    assert response.status_code == 200
    assert DoorDevice.objects.get(id=door_device.id).company.name == company.name


@mark.django_db
def test_door_device_delete(client):
    client_login(client, is_admin=True)

    company = CompanyFactory()
    door_device = DoorDeviceFactory(company=company)

    payload = payload_from_form(DoorDeviceForm(instance=door_device), delete=True)
    response = client.post(reverse('admin_door_devices'), payload)

    assert response.status_code == 200

    assert DoorDevice.objects.filter(id=door_device.id).count() == 0
    assert Company.objects.filter(id=company.id).count() == 1


@mark.django_db
def test_company_delete(client):
    client_login(client, is_admin=True)

    company = CompanyFactory()
    user = UserFactory(company=company)

    payload = payload_from_form(CompanyForm(instance=company), delete=True)
    response = client.post(reverse('admin_companies'), payload)

    assert response.status_code == 200

    assert Company.objects.filter(id=company.id).count() == 0
    assert User.objects.filter(id=user.id).count() == 0
