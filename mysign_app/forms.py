from django import forms
from django.forms import ModelForm

from mysign_app.models import Company, DoorDevice, User


class ReadonlyToggleableForm(ModelForm):
    _readonly = False

    def __init__(self, *args, readonly=False, **kwargs):
        super().__init__(*args, **kwargs)
        

        if self._readonly:
            for field in self.fields:
                self.fields[field].widget = forms.TextInput(attrs={'readonly': True})

    @property
    def readonly(self):
        return self._readonly

    @classmethod
    def as_readonly(cls):
        cls._readonly = True
        return cls


class NoDeleteToggleableForm(ModelForm):
    _nodelete = False

    def __init__(self, *args, _nodelete=False, **kwargs):
        super().__init__(*args, **kwargs)
        

    @property
    def nodelete(self):
        return self._nodelete

    @classmethod
    def as_nodelete(cls):
        cls._nodelete = True
        return cls


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
        fields = ['first_name', 'last_name', 'username', 'company', 'is_admin']


class AddCompanyUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', ]


class CompanyViewForm(NoDeleteToggleableForm):
    class Meta:
        model = Company
        fields = ['name', 'email', 'phone_number', 'website', 'logo', 'color']
