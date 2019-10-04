from colorfield.fields import ColorWidget
from django import forms
from django.forms import ModelForm

from mysign_app.models import Company, DoorDevice, User


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

        for field in self.fields:
            print(field, self.fields[field].widget)

    @property
    def no_delete(self):
        return self._no_delete


class CompanyForm(ReadonlyToggleableForm):
    class Meta:
        model = Company
        fields = ['name', 'email']


class DoorDeviceForm(ModelForm):
    class Meta:
        model = DoorDevice
        fields = ['company', 'id']


class UserForm(NoDeleteToggleableForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'company', 'is_admin']


class AddCompanyUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', ]


class CompanyViewForm(NoDeleteToggleableForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone_number', 'website', 'logo', 'color']
        widgets = {
            'color': ColorWidget()
        }
