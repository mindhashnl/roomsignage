from django.urls import reverse
from pytest import mark

from mysign_app.tests.routes.authentication_helpers import is_company_route


@mark.django_db
def test_index(client):
    is_company_route(client, reverse('company_index'))
