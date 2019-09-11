import random
import string
from datetime import datetime, timedelta

from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import OneToOneField, ForeignKey

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: '+999999999'. Up to 15 digits allowed.")

pairing_code_regex = RegexValidator(regex=r'^\w{4}$', message="Pairing code should be 4 letters")


def generate_pairing_code():
    letters = string.ascii_letters
    return ''.join(random.choice(letters) for i in range(4))


def generate_secret():
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(32))


def expire_default():
    return datetime.now() + timedelta(days=2)


class Company(models.Model):
    name = models.CharField(max_length=50, null=False)
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    email = models.EmailField(max_length=50, null=False)
    website = models.CharField(max_length=50)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class DoorDevice(models.Model):
    company = ForeignKey('Company', on_delete=models.CASCADE)
    room_number = models.IntegerField(null=False, unique=True)

    # Read only fields
    pairing_code = models.CharField(validators=[pairing_code_regex], max_length=4, unique=True,
                                    default=generate_pairing_code)
    pairing_code_expire_at = models.DateTimeField(default=expire_default)
    secret = models.CharField(default=generate_secret, max_length=32, null=False)

    def regenerate_codes(self):
        self.pairing_code = generate_pairing_code()
        self.pairing_code_expire_at = expire_default()
        self.secret = generate_secret()

        self.save()

    def __str__(self):
        return f"{self.room_number} - {self.company.name}"
