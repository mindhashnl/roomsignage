from pytest import mark

from mysign_app.management.commands.seed import Command
from mysign_app.models import Company, DoorDevice, User
from mysign_app.tests.factories import CompanyFactory


@mark.django_db
def test_objects_are_seeded():
    # Run seeds
    Command().handle()

    assert Company.objects.count() == 20
    assert DoorDevice.objects.count() == 20

    assert User.objects.filter(email='hmo@utsign.nl').count() == 1
    assert User.objects.filter(email='hmo@utsign.nl').first().check_password('123456')

    assert User.objects.filter(email='company@utsign.nl').count() == 1
    assert User.objects.filter(email='company@utsign.nl').first().check_password('123456')
    assert User.objects.filter(email='company@utsign.nl').first().company_id

    assert User.objects.filter(email='developer@utsign.nl').count() == 1
    assert User.objects.filter(email='developer@utsign.nl').first().check_password('123456')
    assert User.objects.filter(email='developer@utsign.nl').first().is_staff
    assert User.objects.filter(email='developer@utsign.nl').first().is_superuser


@mark.django_db
def test_database_is_cleared():
    CompanyFactory.create(name="really awesome company")

    # Run seeds
    Command().handle()

    assert Company.objects.filter(name="really awesome company").count() == 0
