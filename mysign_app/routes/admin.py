from django.contrib import messages
from django.contrib.auth.decorators import login_required

from mysign_app.forms import CompanyForm, UserForm, DoorDeviceForm, AddCompanyUserForm
from mysign_app.models import DoorDevice, Company, User

from django.contrib.auth.views import logout_then_login
from django.http import HttpResponse
from django.template import loader

from mysign_app.routes.helpers import admin_required


@login_required
def index(request):
    # TODO: add some custom HMO VS company logic
    template = loader.get_template('mysign_app/admin/index.html')
    return HttpResponse(template.render({}, request))


def logout(request):
    messages.success(request, 'You were successfully logged-out.')
    return logout_then_login(request)


@admin_required
def door_devices(request):
    template = loader.get_template('mysign_app/admin/door_devices.html')
    devices = DoorDevice.objects.all()
    context = {
        'device_list': devices,
        'form': DoorDeviceForm()
    }
    return HttpResponse(template.render(context, request))


@admin_required
def companies(request):
    template = loader.get_template('mysign_app/admin/companies.html')
    companies = Company.objects.all()
    context = {
        'companies': companies,
        'form': CompanyForm()
    }
    return HttpResponse(template.render(context, request))


@admin_required
def users(request):
    template = loader.get_template('mysign_app/admin/users.html')
    users = User.objects.all()
    context = {
        'users': users,
        'form': UserForm()
    }
    return HttpResponse(template.render(context, request))


@admin_required
def addCompany(request):
    template = loader.get_template('mysign_app/admin/addCompany.html')
    context = {
        'AddCompanyUserForm': AddCompanyUserForm(),
        'company_form': CompanyForm(),
    }
    return HttpResponse(template.render(context, request))
