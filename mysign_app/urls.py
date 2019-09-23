from django.urls import path

from .routes.screen import index as screen_index

urlpatterns = [
    path('', screen_index, name='screen'),
]
