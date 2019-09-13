from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from .models import DoorDevice


def screen(request):
    if request.COOKIES.get('screen_secret'):
        device = DoorDevice.objects.filter(secret=request.COOKIES.get('screen_secret')).first()
        if not device:
            # Incorrect secret, unset secret
            response = HttpResponseRedirect('/screen')
            response.delete_cookie('screen_secret')
            return response
    else:
        device = DoorDevice()
        device.save()

    template = loader.get_template('callsign_app/screen.html')
    context = {
        'device': device
    }
    if device.company:
        context['title'] = f'Callsign - {device.company}'
    response = HttpResponse(template.render(context, request))
    response.set_cookie('screen_secret', device.secret)
    return response
