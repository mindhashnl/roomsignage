from django.http import HttpResponse, HttpResponseRedirect
from django.template import loader

from mysign_app.models import DoorDevice


def index(request):
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

    template = loader.get_template('mysign_app/screen.html')
    context = {
        'device': device
    }
    response = HttpResponse(template.render(context, request))
    response.set_cookie('screen_secret', device.secret, max_age=60 * 60 * 24 * 365 * 5)
    return response
