from django.contrib.auth.views import LoginView
from django.urls import path
from .routes import screen_index, admin

urlpatterns = [
    path('', screen_index, name='screen'),

    path('admin/login/', LoginView.as_view(), name='login'),
    path('admin/logout/', admin.logout, name='logout'),

    path('admin/', admin.index, name='admin_index'),

    path('admin/door_devices', admin.door_devices, name='admin_door_devices'),
    path('admin/companies', admin.companies, name='admin_companies'),
    path('admin/users', admin.users, name='admin_users'),

]
