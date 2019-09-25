from mysign_app.management.commands.seed import Command
from mysign_app.models import Company, DoorDevice, User
from mysign_app.tests.factories import CompanyFactory


def test_objects_are_seeded():
    # Run seeds
    Command().handle()

    assert Company.objects.count() == 5
    assert DoorDevice.objects.count() == 20

    assert User.objects.filter(username='HMO').count() == 1
    assert User.objects.filter(username='HMO').first().check_password('123456')

    assert User.objects.filter(username='company').count() == 1
    assert User.objects.filter(username='company').first().check_password('123456')
    assert User.objects.filter(username='company').first().company_id

    assert User.objects.filter(username='developer').count() == 1
    assert User.objects.filter(username='developer').first().check_password('123456')
    assert User.objects.filter(username='developer').first().is_staff
    assert User.objects.filter(username='developer').first().is_superuser


def test_database_is_cleared():
    CompanyFactory.create(name="really awesome company")

    # Run seeds
    Command().handle()

    assert Company.objects.filter(name="really awesome company").count() == 0
