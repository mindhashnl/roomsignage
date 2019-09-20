from django.urls import reverse
from pytest import mark


@mark.django_db
def test_loads(client):
    response = client.get(reverse('screen'))

    assert response.status_code == 200
