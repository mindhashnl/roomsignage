from django.urls import re_path

from . import consumers

websocket_urlpatterns = [
    re_path(r'ws/screen/(?P<screen_id>\w+)/$', consumers.ScreenConsumer),
]
