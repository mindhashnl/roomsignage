import json

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.tokens import PasswordResetTokenGenerator
from django.contrib.auth.views import logout_then_login
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template import loader
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from django.views.generic import FormView, TemplateView
from templated_email import send_templated_mail

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


class DataTablesView(TemplateView, FormView):
    """
    View for displaying datatables and a form on one page
    """
    template_name = 'mysign_app/admin/datatable.html'
    model = None
    form_class = None
    form_kwargs = None
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

    def get_form_kwargs(self):
        kwargs = super().get_form_kwargs()
        if self.form_kwargs:
            kwargs.update(self.form_kwargs)
        return kwargs

    def models_json(self):
        objects = self._all_objects().values(*self.json_fields)
        objects = list(objects)
        return json.dumps(objects)

    def _all_objects(self):
        return self.model.objects.all()


class DoorDevices(AdminRequiredMixin, DataTablesView):
    model = DoorDevice
    form_class = DoorDeviceForm
    list_fields = ['id']
    json_fields = ['id', 'company']


class Companies(AdminRequiredMixin, DataTablesView):
    model = Company
    form_class = CompanyForm
    form_kwargs = {'readonly': True}
    list_fields = ['name']
    json_fields = ['name', 'email', 'phone_number', 'id']


class Users(AdminRequiredMixin, DataTablesView):
    model = User
    form_class = UserForm
    form_kwargs = {'no_delete': True}
    list_fields = ['id', 'first_name', 'last_name']
    json_fields = ['id', 'first_name', 'last_name', 'username', 'company', 'is_admin']


@admin_required
def company_add(request):
    if request.method == 'POST':
        company_form = CompanyForm(request.POST, prefix='company')
        user_form = AddCompanyUserForm(request.POST, prefix='user')
        if company_form.is_valid() and user_form.is_valid():
            company = company_form.save()
            user = user_form.save()
            user.company = company
            user.save()
            send_templated_mail(template_name="welcome_mail",
                                from_email="Gebouw-N <info@utsign.com",
                                recipient_list=[user_form.cleaned_data['email']],
                                context={
                                    'naam': user.first_name + " "
                                    + user.last_name,
                                    'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                                    'token':
                                        PasswordResetTokenGenerator().make_token(
                                        user=user),
                                })

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
