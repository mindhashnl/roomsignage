from django.contrib.auth.views import LoginView
from django.urls import path

from .routes import screen_index, admin

urlpatterns = [
    path('', screen_index, name='screen'),
    path('admin/', admin.index, name='admin_index'),

    path('admin/login/', LoginView.as_view(), name='login'),
    path('admin/logout/', admin.logout, name='logout'),
]
