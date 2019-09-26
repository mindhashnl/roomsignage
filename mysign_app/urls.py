from django.contrib.auth.views import LoginView
from django.urls import path

from .routes import admin, screen_index

urlpatterns = [
    path('', screen_index, name='screen'),

    path('admin/login/', LoginView.as_view(), name='login'),
    path('admin/logout/', admin.logout, name='logout'),

    path('admin/', admin.index, name='admin_index'),

    path('admin/door_devices/', admin.door_devices, name='admin_door_devices'),
    path('admin/companies/', admin.companies, name='admin_companies'),
    path('admin/company', admin.company_add, name='admin_company'),  # TODO link this to the company page
    path('admin/companies/add/', admin.company_add, name='admin_company_add'),
    path('admin/users/', admin.users, name='admin_users'),

]
