from django.contrib.auth.views import LoginView
from django.urls import path

from .routes import admin, company, screen_index

urlpatterns = [
    path('', screen_index, name='screen'),

    path('admin/login/', LoginView.as_view(), name='login'),
    path('admin/logout/', admin.logout, name='logout'),

    path('admin/', admin.index, name='admin_index'),

    path('admin/door_devices/', admin.DoorDevices.as_view(), name='admin_door_devices'),
    path('admin/companies/', admin.Companies.as_view(), name='admin_companies'),
    path('admin/companies/add/', admin.company_add, name='admin_company_add'),
    path('admin/users/', admin.Users.as_view(), name='admin_users'),

    path('company/', company.index, name='company_index'),

    path('company/view', company.company_view, name='company_view'),
    path('company/logout/', company.logout, name='logout'),
    path('company/login/', LoginView.as_view(), name='login'),
]
