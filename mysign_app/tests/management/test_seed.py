from pytest import mark

from mysign_app.management.commands.seed import seed, clear_data
from mysign_app.models import Company, DoorDevice, User


@mark.django_db
def test_company_is_seeded():
    seed()

    assert Company.objects.count() == 5


@mark.django_db
def test_door_device_is_seeded():
    seed()

    assert DoorDevice.objects.count() == 20


@mark.django_db
def test_user_is_seeded():
    seed()

    assert User.objects.filter(username='HMO').count() == 1
    assert User.objects.filter(username='HMO').first().check_password('123456')

    assert User.objects.filter(username='company').count() == 1
    assert User.objects.filter(username='company').first().check_password('123456')
    assert User.objects.filter(username='company').first().company_id

    assert User.objects.filter(username='developer').count() == 1
    assert User.objects.filter(username='developer').first().check_password('123456')
    assert User.objects.filter(username='developer').first().is_staff
    assert User.objects.filter(username='developer').first().is_superuser


@mark.django_db
def test_database_is_cleared():
    seed()
    clear_data()

    assert Company.objects.count() == 0
    assert DoorDevice.objects.count() == 0
    assert User.objects.count() == 0
