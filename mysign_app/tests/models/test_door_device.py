import pytest
from django.core.exceptions import ValidationError
from pytest import mark

from ...models import DoorDevice
from ..factories import DoorDeviceFactory


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
