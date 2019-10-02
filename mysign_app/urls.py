from django.urls import path, include
from django.views.generic import RedirectView, TemplateView

from mysign_app.routes import login

from .routes import admin, company, screen_index

urlpatterns = [
    path('', TemplateView.as_view(template_name='mysign_app/index.html'), name='index'),
    path('screen/', screen_index, name='screen'),

    path('login/', login.Login.as_view(), name='login'),
    path('logout/', login.logout, name='logout'),

    path('accounts/', include('django.contrib.auth.urls')),

    path('admin/', RedirectView.as_view(url='/admin/door_devices/', permanent=False), name='admin_index'),
    path('admin/door_devices/', admin.DoorDevices.as_view(), name='admin_door_devices'),
    path('admin/companies/', admin.Companies.as_view(), name='admin_companies'),
    path('admin/companies/add/', admin.company_add, name='admin_company_add'),
    path('admin/users/', admin.Users.as_view(), name='admin_users'),

    path('company/', company.CompanyIndex.as_view(), name='company_index'),

    path('robots.txt/', TemplateView.as_view(template_name="mysign_app/robots.txt", content_type='text/plain')),
]
