from django.urls import path
from django.views.generic import TemplateView

from mysign_app.routes import admin
from mysign_app.routes.admin import IndexView, logout, login
from django.contrib.auth import views as auth_views
from .routes.screen import index as screen_index

urlpatterns = [
    path('', screen_index, name='screen'),
    path('admin', IndexView.as_view(), name='admin_index'),
    path('admin/login', auth_views.auth_login, name='admin_login'),
    path('admin/door_devices', admin.index, name='admin_door_device'),
    path('admin/companies', admin.companies, name='admin_companies'),
]
