from mysign_app.models import User
from mysign_app.tests.factories import CompanyFactory


def client_login(client, **user_kwargs):
    client.logout()
    User.objects.filter(email='test@user.nl').delete()

    user = User.objects.create_user(email='test@user.nl', password='1234', **user_kwargs)
    client.login(username='test@user.nl', password='1234')

    return user


def _test_unauthenticated(client, route):
    """
      Test that the route is redirected to login when not logged in
    """
    response = client.get(route)

    assert response.status_code == 302
    assert response.url.startswith('/login')


def is_authenticated_route(client, route):
    """
        Test that the route is only accessible with a logged in user
    """
    _test_unauthenticated(client, route)

    client_login(client)
    response = client.get(route)

    assert response.status_code == 200


def is_admin_route(client, route):
    """
        Test that the route is only accessible with a admin user
    """
    _test_unauthenticated(client, route)

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
    _test_unauthenticated(client, route)

    client_login(client)
    response = client.get(route)

    assert response.status_code == 403

    company = CompanyFactory()
    client_login(client, company=company)
    response = client.get(route)

    assert response.status_code == 200
