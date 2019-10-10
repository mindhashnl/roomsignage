from django.urls import reverse
from pytest import mark

from mysign_app.forms import CompanyViewForm
from mysign_app.models import Company
from mysign_app.tests.factories import CompanyFactory
from mysign_app.tests.routes.authentication_helpers import (client_login,
                                                            is_company_route)
from mysign_app.tests.routes.form_helpers import payload_from_form


@mark.django_db
def test_index(client):
    is_company_route(client, reverse('company_index'))


@mark.django_db
def test_update(client):
    company = CompanyFactory()
    client_login(client, company=company)

    company.name = 'New name'
    payload = payload_from_form(CompanyViewForm(instance=company))
    response = client.post(reverse('company_index'), payload)

    assert response.status_code == 200


@mark.django_db
def test_update_other_company(client):
    company = CompanyFactory()
    client_login(client, company=company)

    other_company = CompanyFactory()
    other_company.name = 'New name'
    payload = payload_from_form(CompanyViewForm(instance=other_company))
    response = client.post(reverse('company_index'), payload)

    assert response.status_code == 403
