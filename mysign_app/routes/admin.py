from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.http import HttpResponse
from django.template import loader


@login_required
def index(request):
    # TODO: add some custom HMO VS company logic
    template = loader.get_template('mysign_app/admin/index.html')
    return HttpResponse(template.render({}, request))


def logout(request):
    messages.success(request, 'You were successfully logged-out.')
    return logout_then_login(request)
