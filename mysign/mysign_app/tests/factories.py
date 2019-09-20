import random
import string

import factory
from .. import models


def fake_phone_number():
    return '+31' + ''.join(random.choice(string.digits) for i in range(8))


class CompanyFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.Company

    name = factory.Faker('name')
    phone_number = factory.Faker('msisdn')
    email = factory.Faker('ascii_company_email')
    website = factory.Faker('url')


class DoorDeviceFactory(factory.DjangoModelFactory):
    class Meta:
        model = models.DoorDevice

    company = factory.RelatedFactory(CompanyFactory)
    secret = factory.Faker('password', length=32)
