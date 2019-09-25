import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required

from mysign_app.forms import CompanyForm, UserForm, DoorDeviceForm
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
    template = loader.get_template('mysign_app/admin/base.html')
    devices = DoorDevice.objects.all()
    list_fields = ['id']
    context = {
        'json': json.dumps(list(devices.values('id'))),
        'models': companies,
        'list_fields': list_fields,
        'form': DoorDeviceForm()
    }
    return HttpResponse(template.render(context, request))


@admin_required
def companies(request):
    template = loader.get_template('mysign_app/admin/base.html')
    companies = Company.objects.all()
    list_fields = ['name', 'email']
    context = {
        'json': json.dumps(list(companies.values('name', 'email', 'phone_number'))),
        'models': companies,
        'list_fields': list_fields,
        'form': CompanyForm()
    }
    return HttpResponse(template.render(context, request))


@admin_required
def users(request):
    template = loader.get_template('mysign_app/admin/base.html')
    users = User.objects.all()
    list_fields = ['first_name', 'last_name']
    context = {
        'json': json.dumps(list(users.values('first_name', 'last_name', 'email', 'is_admin', 'company'))),
        'models': users,
        'list_fields': list_fields,
        'form': UserForm()
    }
    return HttpResponse(template.render(context, request))
