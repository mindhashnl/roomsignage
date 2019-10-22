from django.core.management.base import BaseCommand
from django_seed import Seed
from faker import Faker

from mysign_app.models import Company, DoorDevice, User


class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--production', action='store_true')

    def handle(self, *args, **options):
        if options.get('production'):
            self.stdout.write('seeding production data...')
            seed_production()
        else:
            self.stdout.write('clearing database...')
            clear_data()
            self.stdout.write('seeding data...')
            seed()
        self.stdout.write('done.')


def seed():
    seeder = Seed.seeder()

    seeder.add_entity(Company, 20, {'logo': None})
    seeder.add_entity(DoorDevice, 20)
    seeder.execute()

    users = [{'email': 'developer@utsign.nl', 'is_staff': True, 'is_superuser': True},
             {'email': 'HMO@utsign.nl', 'is_admin': True},
             {'email': 'company@utsign.nl', 'company': Company.objects.first()},
             {'email': 'nonlogin@utsign.nl'}]

    fake = Faker()
    for u in users:
        us = User(**u)
        us.first_name = fake.first_name()
        us.last_name = fake.last_name()
        us.set_password('123456')
        us.save()


def seed_production():
    us = User()
    us.email = 'HMO@utsign.nl'
    us.is_admin = True
    us.first_name = 'HMO'
    us.last_name = 'User'
    us.set_password('R34llyS4ve')
    us.save()


def clear_data():
    DoorDevice.objects.all().delete()
    User.objects.all().delete()
    Company.objects.all().delete()
