import random
import string
import uuid

from colorfield.fields import ColorField
from django.contrib.auth.models import AbstractUser
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import ForeignKey

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: "
                                     "'+999999999'. Up to 15 digits allowed.")


def generate_secret():
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(32))


def logo_upload(instance, filename):
    name, extension = filename.split('.', 1)
    return f"companies/logos/{uuid.uuid4()}.{extension}"


class User(AbstractUser):
    company = ForeignKey('Company', on_delete=models.DO_NOTHING, null=True)


class Company(models.Model):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    email = models.EmailField(max_length=50)
    website = models.URLField(max_length=50)
    logo = models.ImageField(upload_to=logo_upload, blank=True)
    color = ColorField(blank=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class DoorDevice(models.Model):
    company = ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    secret = models.CharField(default=generate_secret, max_length=32, null=False)