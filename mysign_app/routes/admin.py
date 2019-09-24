from django.contrib import messages
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import login_required, user_passes_test
from django.contrib.auth.views import logout_then_login
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.template import loader

from mysign_app.routes.helpers import admin_required, company_required


@login_required
def index(request):
    # TODO: add some custom HMO VS company logic
    template = loader.get_template('mysign_app/admin/index.html')
    return HttpResponse(template.render({}, request))


@admin_required
def admin(request):
    # TEMPORARY ADMIN ROUTE, PLEASE REMOVE WHEN REAL PAGES ARE IMPLEMENTED
    return HttpResponse('Temporary admin page. Should be replaced by real pages', content_type="text/plain")


@company_required
def company(request):
    # TEMPORARY COMPANY ROUTE, PLEASE REMOVE WHEN REAL PAGES ARE IMPLEMENTED
    return HttpResponse('Temporary company page. Should be replaced by real pages', content_type="text/plain")


def logout(request):
    messages.success(request, 'You were successfully logged-out.')
    return logout_then_login(request)
