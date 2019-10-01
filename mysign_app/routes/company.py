from django.contrib.messages.views import SuccessMessageMixin
from django.views.generic import UpdateView

from mysign_app.forms import CompanyViewForm
from mysign_app.models import Company
from mysign_app.routes.helpers import CompanyRequiredMixin


class CompanyIndex(CompanyRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'mysign_app/company/base.html'
    success_message = 'Company succesfully updated'
    success_url = '/company/'
    model = Company
    form_class = CompanyViewForm

    def get_object(self, queryset=None):
        return self.model.objects.get(id=self.request.user.company.id)
