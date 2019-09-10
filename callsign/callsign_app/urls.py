from django.urls import path

from . import views

urlpatterns = [
    path('screen/', views.screen, name='screen'),
    path('door_devices/', views.DoorDeviceIndex.as_view(), name='screen'),
    path('unpair/', views.unpair, name='screen'),
]