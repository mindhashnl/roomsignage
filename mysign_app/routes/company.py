from mysign_app.forms import CompanyViewForm
from mysign_app.models import Company
from mysign_app.routes.admin import AdministrationView
from mysign_app.routes.helpers import CompanyRequiredMixin


class CompanyIndex(AdministrationView, CompanyRequiredMixin):
    template_name = 'mysign_app/company/base.html'
    model = Company
    form_class = CompanyViewForm
