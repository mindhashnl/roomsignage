import datetime

from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.template import loader
from django.views import generic

from .models import DoorDevice


class DoorDeviceIndex(generic.ListView):
    template_name = 'callsign_app/door_device_index.html'
    context_object_name = 'devices'

    def get_queryset(self):
        return DoorDevice.objects.all()


def _screen_response(device, request):
    company = device.company
    template = loader.get_template('callsign_app/screen.html')
    context = {
        'company': company,
    }
    response = HttpResponse(template.render(context, request))
    response.set_cookie('screen_secret', device.secret)
    return response


def screen(request):
    if request.COOKIES.get('screen_secret'):
        device = DoorDevice.objects.filter(secret=request.COOKIES.get('screen_secret')).first()
        if not device:
            return HttpResponseRedirect('/unpair')
        else:
            return _screen_response(device, request)

    if request.GET.get('pairing_code'):
        device = DoorDevice.objects.all().filter(pairing_code=request.GET.get('pairing_code'),
                                                 pairing_code_expire_at__gt=datetime.datetime.now()).first()
        if not device:
            raise Http404("Wrong or expired pairing code entered")
        else:
            return _screen_response(device, request)

    return HttpResponse(loader.get_template('callsign_app/pair_screen.html').render({}, request))


def unpair(request):
    response = HttpResponseRedirect('/screen')
    response.delete_cookie('screen_secret')
    return response
