from django.urls import reverse
from pytest import mark

from mysign_app.tests.factories import CompanyFactory
from mysign_app.tests.routes.authentication_helpers import (
    _test_unauthenticated, client_login)


@mark.django_db
def test_index_admin(client):
    _test_unauthenticated(client, reverse('company_index'))

    client_login(client, is_admin=True)
    response = client.get(reverse('company_index'))

    assert response.status_code == 302
    assert response.url == reverse('admin_door_devices')


@mark.django_db
def test_index_company(client):
    _test_unauthenticated(client, reverse('company_index'))

    company = CompanyFactory()
    client_login(client, company=company)
    response = client.get(reverse('company_index'))

    assert response.status_code == 302
    assert response.url == reverse('company_view')
