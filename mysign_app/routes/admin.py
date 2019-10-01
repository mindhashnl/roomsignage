from django.contrib import messages
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader

from mysign_app.forms import (AddCompanyUserForm, CompanyForm, DoorDeviceForm,
                              UserForm)
from mysign_app.models import Company, DoorDevice, User
from mysign_app.routes.helpers import AdminRequiredMixin, admin_required

from .authenticated import AuthenticatedView


class AdminView(AdminRequiredMixin, AuthenticatedView):
    pass


class DoorDevices(AdminView):
    model = DoorDevice
    form_class = DoorDeviceForm
    list_fields = ['id']
    json_fields = ['id', 'company']


class Companies(AdminView):
    model = Company
    form_class = CompanyForm.as_readonly()
    list_fields = ['name']
    json_fields = ['name', 'email', 'phone_number', 'id']


class Users(AdminView):
    model = User
    form_class = UserForm.as_nodelete()
    list_fields = ['id', 'first_name', 'last_name']
    json_fields = ['id', 'first_name', 'last_name', 'username', 'company', 'is_admin']


@admin_required
def company_add(request):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST, prefix='company')
        user_form = AddCompanyUserForm(request.POST, prefix='user')
        if company_form.is_valid() and user_form.is_valid():
            company_form.save()
            user_form.save()
            messages.info(request, 'Company and user successfully added')
            return redirect('admin_companies')
    else:
        company_form = CompanyForm(prefix='company')
        user_form = AddCompanyUserForm(prefix='user')

    template = loader.get_template('mysign_app/admin/company_add.html')
    context = {
        'user_form': user_form,
        'company_form': company_form,
    }
    return HttpResponse(template.render(context, request))
