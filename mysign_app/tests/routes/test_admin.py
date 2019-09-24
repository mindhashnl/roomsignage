from django.urls import reverse
from pytest import mark

from mysign_app.tests.routes.helpers import is_authenticated_route, is_admin_route, is_company_route, client_login


@mark.django_db
def test_index(client):
    is_authenticated_route(client, reverse('admin_index'))


@mark.django_db
def test_admin(client):
    is_admin_route(client, reverse('admin_admin'))


@mark.django_db
def test_company(client):
    is_company_route(client, reverse('admin_company'))


@mark.django_db
def test_logout(client):
    """ User is logged out """
    client_login(client)
    assert '_auth_user_id' in client.session

    response = client.get(reverse('logout'))

    assert response.status_code == 302
    assert response.url == '/admin/login'
    assert '_auth_user_id' not in client.session
