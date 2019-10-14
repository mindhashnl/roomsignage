import chromedriver_binary  # noqa: F401
from django.conf import settings
from django.conf.global_settings import SESSION_COOKIE_NAME
from django.contrib.auth import (BACKEND_SESSION_KEY, HASH_SESSION_KEY,
                                 SESSION_KEY)
from django.contrib.sessions.backends.db import SessionStore

from mysign_app.models import User


def authenticate_selenium(selenium, live_server, **user_kwargs):
    user = User.objects.create_user(email='test@user.nl', password='1234', **user_kwargs)

    session = SessionStore()
    session[SESSION_KEY] = user.pk
    session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()

    selenium.get(live_server.url)
    selenium.add_cookie({'name': SESSION_COOKIE_NAME, 'value': session.session_key, 'secure': False, 'path': '/'})
