import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from ...models import DoorDevice
from ..factories import CompanyFactory, DoorDeviceFactory


@mark.django_db
def test_create():
    door_device = DoorDeviceFactory()
    door_device.full_clean()
    assert DoorDevice.objects.count() == 1


@mark.django_db
def test_secret_required():
    door_device = DoorDeviceFactory.build(secret="")

    with pytest.raises(ValidationError):
        assert not door_device.full_clean()


def test_str():
    company = CompanyFactory.build(name="test")
    door_device = DoorDeviceFactory.build(id=1)

    assert str(door_device) == "1"

    door_device.company = company

    assert str(door_device) == "test"


def test_class_name():
    assert DoorDevice.class_name() == 'Door Device'
