import random
import string

import factory

from mysign_app.models import User

from .. import models


def fake_phone_number():
    return '+31' + ''.join(random.choice(string.digits) for i in range(8))


class UserFactory(factory.DjangoModelFactory):
    class Meta:
        model = User

    first_name = factory.Faker('first_name')
    last_name = factory.Faker('last_name')
    password = factory.Faker('password')
    email = factory.Faker('email')


class CompanyFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Company

    name = factory.Faker('name')
    phone_number = factory.Faker('msisdn')
    email = factory.Faker('ascii_company_email')
    website = factory.Faker('url')
    logo = factory.django.ImageField(color='blue')
    image = factory.django.ImageField(color='blue')


class DoorDeviceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.DoorDevice

    company = factory.RelatedFactory(CompanyFactory)
    secret = factory.Faker('password', length=32)
