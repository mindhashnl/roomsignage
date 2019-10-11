import os
from asyncio import sleep
from datetime import date, time

from django.conf import settings
import pytest
import chromedriver_binary
from django.conf.global_settings import SESSION_COOKIE_NAME
from django.contrib.auth import SESSION_KEY, BACKEND_SESSION_KEY, HASH_SESSION_KEY
from django.contrib.sessions.backends.db import SessionStore
from selenium import webdriver
from pytest import mark

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
