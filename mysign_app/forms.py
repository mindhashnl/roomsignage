from django.forms import ModelForm

from mysign_app.models import Company, User, DoorDevice


class CompanyForm(ModelForm):
    class Meta:
        model = Company
        fields = ['name', 'email']


class DoorDeviceForm(ModelForm):
    class Meta:
        model = DoorDevice
        fields = ['company', 'id']


class UserForm(ModelForm):
    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username', 'company', 'is_admin']
