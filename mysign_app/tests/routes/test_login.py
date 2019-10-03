from django.urls import reverse
from pytest import mark

from mysign_app.models import User
from mysign_app.tests.factories import CompanyFactory
from mysign_app.tests.routes.authentication_helpers import client_login
from mysign_app.tests.routes.helpers import messages_to_list


def create_user(**kwargs):
    User.objects.create_user(email='info@example.com',
                             password='123456',
                             **kwargs)

"""
On all tests the payload contain username, however this matches with the email field on the model
"""

@mark.django_db
def test_login_wrong_credentials(client):
    create_user()

    response = client.post(reverse('login'), {'username': 'info@example.com', 'password': 'wrong_password!'})

    assert response.status_code == 200
    assert '_auth_user_id' not in client.session


@mark.django_db
def test_login_correct_credentials(client):
    """ When with correct credentials but no staff/company/admin configured login is not possible"""
    create_user()

    response = client.post(reverse('login'), {'username': 'info@example.com', 'password': '123456'})
    messages = messages_to_list(response)

    assert response.status_code == 302
    assert messages[0] == 'We cannot idenitify the usertype of this user. ' \
                          'Please check that this user is configured as staff, admin or company user.'
    assert '_auth_user_id' not in client.session


@mark.django_db
def test_login_admin(client):
    create_user(is_admin=True)

    response = client.post(reverse('login'), {'username': 'info@example.com', 'password': '123456'})

    assert response.status_code == 302
    assert response.url == reverse('admin_door_devices')


@mark.django_db
def test_login_company(client):
    company = CompanyFactory()
    create_user(company=company)

    response = client.post(reverse('login'), {'username': 'info@example.com', 'password': '123456'})

    assert response.status_code == 302
    assert response.url == reverse('company_index')


@mark.django_db
def test_login_staff(client):
    create_user(is_staff=True)

    response = client.post(reverse('login'), {'username': 'info@example.com', 'password': '123456'})

    assert response.status_code == 302
    assert response.url == '/django_admin'


@mark.django_db
def test_logout(client):
    """ User is logged out """
    client_login(client)
    assert '_auth_user_id' in client.session

    response = client.get(reverse('logout'))

    assert response.status_code == 302
    assert response.url == reverse('login')
    assert '_auth_user_id' not in client.session
