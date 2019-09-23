from django.urls import reverse
from pytest import mark


@mark.django_db
def test_index_unauthenticated(client):
    """ Redirect to login when not authenticated"""
    response = client.get(reverse('admin_index'))

    assert response.status_code == 302
    assert response.url == '/admin/login?next=/admin/'


@mark.django_db
def test_index_authenticated(authenticated_client):
    """ Load the path when authenticated"""
    response = authenticated_client.get(reverse('admin_index'))

    assert response.status_code == 200


@mark.django_db
def test_logout(authenticated_client):
    """ User is logged out """
    assert '_auth_user_id' in authenticated_client.session

    response = authenticated_client.get(reverse('logout'))

    assert response.status_code == 302
    assert response.url == '/admin/login'
    assert '_auth_user_id' not in authenticated_client.session
