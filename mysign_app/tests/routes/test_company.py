from django.urls import reverse
from pytest import mark

from mysign_app.models import Company
from mysign_app.tests.factories import CompanyFactory
from mysign_app.tests.routes.authentication_helpers import is_company_route, client_login
from mysign_app.tests.routes.form_helpers import payload_from_form


@mark.django_db
def test_index(client):
    is_company_route(client, reverse('company_index'))


# @mark.django_db
# def test_update(client):
#     company = CompanyFactory()
#     client_login(client, company=company)
#
#     company.name = 'New name'
#     payload = payload_from_form(CompanyFactory(instance=company))
#     response = client.post(reverse('admin_index'), payload)
#
#     assert response.status_code == 200
#     assert Company.objects.get(id=company.id).name == 'New name'
