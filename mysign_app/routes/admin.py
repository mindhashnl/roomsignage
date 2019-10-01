import json

import stringcase
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import logout_then_login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.views.generic import FormView, TemplateView

from mysign_app.forms import (AddCompanyUserForm, CompanyForm, DoorDeviceForm,
                              UserForm)
from mysign_app.models import Company, DoorDevice, User
from mysign_app.routes.helpers import AdminRequiredMixin, admin_required


@login_required
def index(request):
    if request.user.is_admin:
        return redirect('admin_door_devices')
    if request.user.company:
        return redirect('company_view')


def logout(request):
    messages.success(request, 'You were successfully logged-out.')
    return logout_then_login(request)


class AdministrationView(TemplateView, FormView):
    template_name = 'mysign_app/admin/base.html'
    model = None
    form_class = None
    list_fields = []
    json_fields = []

    def post(self, request, *args, **kwargs):
        """ Only clicked buttons get their name send, so this checks if the button with name 'delete' is pressed """
        if request.POST.get("delete"):
            self.model.objects.get(id=request.POST.get('id')).delete()
            messages.success(request, f'{self.model.class_name()} succesfully deleted')
            form = self.form_class()
        else:
            """ Update the model """
            model = self.model.objects.get(id=request.POST.get('id'))
            form = self.form_class(request.POST, instance=model)
            if form.is_valid():
                form.save()
                messages.success(request, f'{self.model.class_name()} succesfully created')
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
        objects = self._all_objects()
        json_objects = []
        # Hacky workaround for relationships
        for o in objects:
            json_object = {}
            for f in self.json_fields:
                if '.' in f:  # If it is an fk field
                    fk_model_name, fk_property = f.split('.')
                    fk_model = getattr(o, fk_model_name)
                    json_object[stringcase.snakecase(f)] = getattr(fk_model, fk_property)
                else:
                    json_object[f] = getattr(o, f)
            json_objects.append(json_object)
        return json.dumps(json_objects)

    def _all_objects(self):
        return self.model.objects.all()


class AdminView(AdminRequiredMixin, AdministrationView):
    pass


class DoorDevices(AdminView):
    model = DoorDevice
    form_class = DoorDeviceForm
    list_fields = ['id', 'company_name']
    json_fields = ['id', 'company.name']


class Companies(AdminView):
    model = Company
    form_class = CompanyForm.as_readonly()
    list_fields = ['name']
    json_fields = ['name', 'email', 'phone_number', 'id']


class Users(AdminView):
    model = User
    form_class = UserForm.as_nodelete()
    list_fields = ['id', 'first_name', 'last_name']
    json_fields = ['id', 'first_name', 'last_name', 'username', 'company', 'is_admin']


@admin_required
def company_add(request):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST, prefix='company')
        user_form = AddCompanyUserForm(request.POST, prefix='user')
        if company_form.is_valid() and user_form.is_valid():
            company_form.save()
            user_form.save()
            messages.info(request, 'Company and user successfully added')
            return redirect('admin_companies')
    else:
        company_form = CompanyForm(prefix='company')
        user_form = AddCompanyUserForm(prefix='user')

    template = loader.get_template('mysign_app/admin/company_add.html')
    context = {
        'user_form': user_form,
        'company_form': company_form,
    }
    return HttpResponse(template.render(context, request))
