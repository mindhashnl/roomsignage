from django.urls import reverse
from pytest import mark

from mysign_app.models import User
from mysign_app.tests.factories import CompanyFactory


def client_login(client, **user_kwargs):
    client.logout()
    User.objects.filter(username='test_user').delete()

    User.objects.create_user(username='test_user', password='1234', **user_kwargs)
    client.login(username='test_user', password='1234')


def is_authenticated_route(client, route):
    """
        Test that the route is only accessible with a logged in user
    """
    response = client.get(route)

    assert response.status_code == 302
    assert response.url.startswith('/admin/login')


def is_admin_route(client, route):
    """
        Test that the route is only accessible with a admin user
    """
    is_authenticated_route(client, route)

    client_login(client)
    response = client.get(route)

    assert response.status_code == 403

    client_login(client, is_admin=True)
    response = client.get(route)

    assert response.status_code == 200


def is_company_route(client, route):
    """
        Test that the route is only accessible with a company user
    """
    is_authenticated_route(client, route)

    client_login(client)
    response = client.get(route)

    assert response.status_code == 403

    company = CompanyFactory()
    client_login(client, company=company)
    response = client.get(route)

    assert response.status_code == 200
