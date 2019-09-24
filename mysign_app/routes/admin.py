from django.contrib import messages
from django.contrib.auth.decorators import login_required
from mysign_app.models import DoorDevice, Company

from django.contrib.auth.views import logout_then_login
from django.http import HttpResponse
from django.template import loader

from mysign_app.routes.helpers import admin_required, company_required


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
        'device_list': devices
    }
    return HttpResponse(template.render(context, request))

@admin_required
def companies(request):
    template = loader.get_template('mysign_app/admin/companies.html')
    companies = Company.objects.all()
    context = {
        'companies': companies
    }
    return HttpResponse(template.render(context, request))
