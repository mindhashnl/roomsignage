from django import forms
from django.forms import ModelForm

from mysign_app.models import Company, DoorDevice, User


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email']
        widgets = {
            'name': forms.TextInput(attrs={'readonly': True}),
            'email': forms.TextInput(attrs={'readonly': True}),
        }


class DoorDeviceForm(ModelForm):
    class Meta:
        model = DoorDevice
        fields = ['company', 'id']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'company', 'is_admin']


class AddCompanyUserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username', ]
