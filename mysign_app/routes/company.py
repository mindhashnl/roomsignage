from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.views.generic import TemplateView, FormView

from mysign_app.forms import CompanyViewForm
from mysign_app.models import Company
from mysign_app.routes.admin import AdministrationView
from mysign_app.routes.helpers import CompanyRequiredMixin


class CompanyIndex(CompanyRequiredMixin, TemplateView, FormView):
    template_name = 'mysign_app/company/base.html'
    model = Company
    form_class = CompanyViewForm

    def post(self, request, *args, **kwargs):
        if request.POST.get('id') != request.user.company.id:
            raise PermissionDenied('Company user can only update own company')

        model = self.model.objects.get(id=request.POST.get('id'))
        form = self.form_class(request.POST, instance=model)
        if form.is_valid():
            form.save()
            messages.success(request, f'{self.model.class_name()} succesfully updated')
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


class CompanyIndex(CompanyRequiredMixin, AdministrationView):
    template_name = 'mysign_app/company/base.html'
    model = Company
    form_class = CompanyViewForm
