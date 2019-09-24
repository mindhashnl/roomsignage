import pytest

from mysign_app.models import User


@pytest.fixture
def authenticated_client(client):
    user = User.objects.create_user(username='test', password='1234', is_admin=True)
    client.login(username=user.username, password='1234')

    return client
