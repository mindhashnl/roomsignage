from django.forms import model_to_dict
from django.urls import reverse
from pytest import mark

from mysign_app.forms import AddCompanyUserForm, CompanyForm
from mysign_app.models import Company, User
from mysign_app.tests.factories import CompanyFactory, UserFactory
from mysign_app.tests.routes.authentication_helpers import (
    client_login, is_admin_route, is_authenticated_route)
from mysign_app.tests.routes.form_helpers import payload_from_form


@mark.django_db
def test_index(client):
    is_authenticated_route(client, reverse('admin_index'))


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
    company_payload = payload_from_form(CompanyForm, CompanyFactory, prefix='company')
    user_payload = payload_from_form(AddCompanyUserForm, UserFactory, prefix='user')
    payload = {**company_payload, **user_payload}

    response = client.post(reverse('admin_company_add'), payload)

    assert response.status_code == 302
    assert response.url == reverse('admin_companies')
    assert Company.objects.count() == 1
    assert User.objects.count() == 2  # One is logged in user, other created user


@mark.django_db
def test_users(client):
    is_admin_route(client, reverse('admin_users'))


@mark.django_db
def test_logout(client):
    """ User is logged out """
    client_login(client)
    assert '_auth_user_id' in client.session

    response = client.get(reverse('logout'))

    assert response.status_code == 302
    assert response.url == '/admin/login'
    assert '_auth_user_id' not in client.session
