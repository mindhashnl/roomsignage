import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.generic import FormView, TemplateView

from mysign_app.forms import (CompanyViewForm)
from mysign_app.routes.helpers import AdminRequiredMixin


@login_required
def index(request):
    if request.user.is_admin:
        return redirect('admin_door_devices')
    if request.user.company:
        return redirect('company_view')


class CompanyView(AdminRequiredMixin, TemplateView, FormView):
    template_name = 'mysign_app/company/base.html'
    model = None
    form_class = None
    list_fields = []
    json_fields = []

    def post(self, request, *args, **kwargs):
        """ Update the model """
        model = self.model.objects.get(id=request.POST.get('id'))
        form = self.form_class(request.POST, instance=model)
        if form.is_valid():
            form.save()
            form = self.form_class()

        context = self.get_context_data(form=form, **kwargs)
        return self.render_to_response(context)

    @property
    def extra_context(self):
        return {
            'models': self._all_objects(),
            'list_fields': self.list_fields,
            'json': self.models_json(),
        }

    def models_json(self):
        objects = self._all_objects().values(*self.json_fields)
        objects = list(objects)
        return json.dumps(objects)

    def _all_objects(self):
        return self.model.objects.all()


def logout(request):
    messages.success(request, 'You were successfully logged-out.')
    return logout_then_login(request)


def company_view(request):
    """if request.method == 'POST':
        form = CompanyViewForm(request.POST, prefix='company_view')
        if form.is_valid():
            form.save()
            messages.info(request, 'Company changed successfully')
            return redirect('admin_company_view')
    else:
        form = CompanyViewForm(prefix='company_view')
"""
    template = loader.get_template('mysign_app/company/company_view.html')
    context = {
        'form': CompanyViewForm,
    }
    return HttpResponse(template.render(context, request))
