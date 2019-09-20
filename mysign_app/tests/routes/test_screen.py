from django.http import SimpleCookie
from django.urls import reverse
from pytest import mark

from mysign_app.models import DoorDevice
from mysign_app.tests.factories import DoorDeviceFactory


@mark.django_db
def test_new_screen(client):
    """ A new door device object is created """
    response = client.get(reverse('screen'))

    assert response.status_code == 200
    assert DoorDevice.objects.count() == 1


@mark.django_db
def test_existing(client):
    """ When requesting with existing door device secret this is loaded """
    door_device = DoorDeviceFactory()

    client.cookies = SimpleCookie({'screen_secret': door_device.secret})
    response = client.get(reverse('screen'))

    assert response.status_code == 200
    assert response.context['device'] == door_device
    assert response.cookies['screen_secret'].value == door_device.secret
    assert DoorDevice.objects.count() == 1


@mark.django_db
def test_wrong_secret(client):
    """ Cookie is removed when a wrong secret is provided """
    client.cookies = SimpleCookie({'screen_secret': 'incorrect!'})
    response = client.get(reverse('screen'))

    assert response.status_code == 302
    assert DoorDevice.objects.count() == 0
