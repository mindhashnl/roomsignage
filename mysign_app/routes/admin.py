from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import logout_then_login
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import redirect
from django.template import loader
from django.views import generic

from mysign_app.models import DoorDevice


class IndexView(LoginRequiredMixin, generic.ListView):
    template_name = 'mysign_app/admin/index.html'
    context_object_name = 'door_devices'

    def get_queryset(self):
        return DoorDevice.objects

def login(request):
    pass

def logout(request):
    messages.success(request, 'You were successfully logged-out.')
    return logout_then_login(request)


def index(request):
    template = loader.get_template('mysign_app/admin/HMO-Overview-Devices.html')
    devices = DoorDevice.objects.all()
    context = {
        'device_list': devices
    }
    return HttpResponse(template.render(context, request))