from django.urls import path
from django.views.generic import RedirectView

from mysign_app.routes import login

from .routes import admin, company, screen_index

urlpatterns = [
    path('', screen_index, name='screen'),

    path('login/', login.Login.as_view(), name='login'),
    path('logout/', login.logout, name='logout'),

    path('admin/', RedirectView.as_view(url='/admin/door_devices/', permanent=False), name='admin_index'),
    path('admin/door_devices/', admin.DoorDevices.as_view(), name='admin_door_devices'),
    path('admin/companies/', admin.Companies.as_view(), name='admin_companies'),
    path('admin/companies/add/', admin.company_add, name='admin_company_add'),
    path('admin/users/', admin.Users.as_view(), name='admin_users'),

    path('company/', company.CompanyIndex.as_view(), name='company_index'),
]
