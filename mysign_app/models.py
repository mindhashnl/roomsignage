import random
import string
import uuid

import stringcase as stringcase
from colorfield.fields import ColorField
from django.core.exceptions import ValidationError
from django.core.validators import RegexValidator
from django.db import models
from django.db.models import BooleanField, ForeignKey
from django.templatetags.static import static
from django_use_email_as_username.models import BaseUser, BaseUserManager

phone_regex = RegexValidator(regex=r'^\+?1?\d{9,15}$',
                             message="Phone number must be entered in the format: "
                                     "'+999999999'. Up to 15 digits allowed.")

domain_regex = RegexValidator(regex=r'(?:[a-z0-9](?:[a-z0-9-]{0,61}[a-z0-9])?\.)+[a-z0-9][a-z0-9-]{0,61}[a-z0-9]',
                              message='This is not a valid domain name.')


def generate_secret():
    letters = string.ascii_letters + string.digits + string.punctuation
    return ''.join(random.choice(letters) for i in range(32))


def logo_upload(instance, filename):
    name, extension = filename.split('.', 1)
    return f"companies/logos/{uuid.uuid4()}.{extension}"


class ClassStr:
    @classmethod
    def class_name(cls):
        return stringcase.sentencecase(cls.__name__)


class CaseInsensitiveFieldMixin:
    """
    Field mixin that uses case-insensitive lookup alternatives if they exist.
    Source: https://ewp.gma.mybluehost.me/2018/10/27/case-insensitive-fields-in-django-models/
    """
    LOOKUP_CONVERSIONS = {
        'exact': 'iexact',
        'contains': 'icontains',
        'startswith': 'istartswith',
        'endswith': 'iendswith',
        'regex': 'iregex',
    }

    def get_lookup(self, lookup_name):
        converted = self.LOOKUP_CONVERSIONS.get(lookup_name, lookup_name)
        return super().get_lookup(converted)


class CIEmailField(CaseInsensitiveFieldMixin, models.EmailField):
    pass


class User(BaseUser, ClassStr):
    company = ForeignKey('Company', on_delete=models.CASCADE, null=True, blank=True)
    is_admin = BooleanField(default=False)
    email = CIEmailField('email', unique=True, blank=False)

    objects = BaseUserManager()

    def clean(self, *args, **kwargs):
        super().clean()
        # Validate company and is_admin not both set
        if self.company and self.is_admin:
            raise ValidationError("Company and is_admin cannot set both")

    def save(self, *args, **kwargs):
        # If this is a new user
        if not self.pk and not self.password:
            password = User.objects.make_random_password()
            self.set_password(password)

        self.full_clean()
        super().save(*args, **kwargs)


class Company(models.Model, ClassStr):
    name = models.CharField(max_length=50)
    phone_number = models.CharField(validators=[phone_regex], max_length=15)
    email = models.EmailField(max_length=50)
    website = models.CharField(max_length=50, validators=[domain_regex])
    logo = models.ImageField(upload_to=logo_upload, blank=True)
    color = ColorField(blank=True)

    def logo_url_or_default(self):
        if self.logo:
            return self.logo.url
        return static('mysign_app/logo-fallback.png')

    @property
    def door_devices(self):
        return DoorDevice.objects.filter(company_id=self.id)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = "Companies"


class DoorDevice(models.Model, ClassStr):
    company = ForeignKey(Company, on_delete=models.CASCADE, blank=True, null=True)
    secret = models.CharField(default=generate_secret, max_length=32, null=False)

    def __str__(self):
        if self.company:
            return self.company.name
        return str(self.id)
