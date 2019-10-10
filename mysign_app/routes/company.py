from django.contrib.messages.views import SuccessMessageMixin
from django.core.exceptions import PermissionDenied
from django.views.generic import UpdateView

from mysign_app.forms import CompanyViewForm
from mysign_app.models import Company
from mysign_app.routes.helpers import CompanyRequiredMixin, refresh_screens


class CompanyIndex(CompanyRequiredMixin, SuccessMessageMixin, UpdateView):
    template_name = 'mysign_app/company/index.html'
    success_message = 'Company succesfully updated'
    success_url = '/company/'
    model = Company
    form_class = CompanyViewForm

    def form_valid(self, form):
        response = super().form_valid(form)
        refresh_screens(self.object)
        return response

    def get_object(self, queryset=None):
        if self.request.POST and int(self.request.POST.get('id')) != self.request.user.company.id:
            raise PermissionDenied("Cannot update company that user is not linked to")
        return self.model.objects.get(id=self.request.user.company.id)
