from colorfield.fields import ColorWidget
from django import forms
from django.core.exceptions import ValidationError
from django.forms import ModelForm

from mysign_app.models import Company, DoorDevice, User


class ModelClassMixin:
    def model_class_name(self):
        return self.instance.__class__.class_name().lower()


class ReadonlyToggleableForm(ModelForm):
    def __init__(self, *args, readonly=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._readonly = readonly

        if self._readonly:
            for field in self.fields:
                self.fields[field].widget = forms.TextInput(attrs={'readonly': True})

    @property
    def readonly(self):
        return self._readonly


class NoDeleteToggleableForm(ModelForm):
    def __init__(self, *args, no_delete=False, **kwargs):
        super().__init__(*args, **kwargs)
        self._no_delete = no_delete

    @property
    def no_delete(self):
        return self._no_delete


class CompanyForm(ReadonlyToggleableForm, ModelClassMixin):
    class Meta:
        model = Company
        fields = ['name', 'email']


class DoorDeviceForm(ModelForm, ModelClassMixin):
    class Meta:
        model = DoorDevice
        fields = ['company', 'id']


class UserForm(NoDeleteToggleableForm, ModelClassMixin):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'company', 'is_admin']

    def __init__(self, *args, **kwargs):
        self.request_user = kwargs.pop('user', None)
        super().__init__(*args, **kwargs)

    def clean(self):
        if self.instance == self.request_user and self.instance.is_admin != self.cleaned_data['is_admin']:
            raise ValidationError('Cannot unset is_admin property on own user', code='invalid_is_admin')
        return super().clean()


class AddCompanyUserForm(ModelForm, ModelClassMixin):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]


class AddUserForm(ModelForm, ModelClassMixin):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'company', 'is_admin']


class CompanyViewForm(NoDeleteToggleableForm, ModelClassMixin):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone_number', 'website', 'logo', 'color', 'text_color']
        widgets = {
            'color': ColorWidget()
        }
