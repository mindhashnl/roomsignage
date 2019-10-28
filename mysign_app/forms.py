from colorfield.fields import ColorWidget
from django import forms
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


class AddCompanyUserForm(ModelForm, ModelClassMixin):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]


class AddUserForm(ModelForm, ModelClassMixin):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'company', 'is_admin']


class CompanyViewForm(ModelForm, ModelClassMixin):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone_number', 'website', 'logo', 'image', 'color', 'text_color']
        widgets = {
            'color': ColorWidget()
        }
