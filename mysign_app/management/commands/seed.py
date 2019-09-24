from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker

from mysign_app.models import Company, DoorDevice, User


class Command(BaseCommand):
    help = "seed database for testing and development."

    def handle(self, *args, **options):
        self.stdout.write('clearing database...')
        clear_data()
        self.stdout.write('seeding data...')
        seed()
        self.stdout.write('done.')


def seed():
    seeder = Seed.seeder()

    seeder.add_entity(Company, 5)
    seeder.add_entity(DoorDevice, 10)
    seeder.execute()

    users = [{'username': 'developer', 'is_staff': True, 'is_superuser': True},
             {'username': 'HMO', 'is_admin': True},
             {'username': 'company', 'company': Company.objects.first()}]

    fake = Faker()
    for u in users:
        us = User(**u)
        us.first_name = fake.first_name()
        us.last_name = fake.last_name()
        us.email = fake.email()
        us.set_password('123456')
        us.save()


def clear_data():
    DoorDevice.objects.all().delete()
    User.objects.all().delete()
    Company.objects.all().delete()
