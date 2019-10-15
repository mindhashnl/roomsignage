import os

from .base import *  # noqa: F401,F403

DEBUG = False
ALLOWED_HOSTS = ['utsign.nl']
SECRET_KEY = os.environ['SECRET_KEY']

# HTTP settings
CSRF_COOKIE_SECURE = True
SESSION_COOKIE_SECURE = True
SECURE_HSTS_SECONDS = 60  # TODO set this value to a higher number (like 1 year)
SECURE_HSTS_INCLUDE_SUBDOMAINS = True

# Security
SECURE_CONTENT_TYPE_NOSNIFF = True
SECURE_BROWSER_XSS_FILTER = True
X_FRAME_OPTIONS = 'DENY'

SENDGRID_SANDBOX_MODE_IN_DEBUG = False

ADMINS = [('Martijn', 'm.h.woudstra@student.utwente.nl'), ('Matthijs', 'm.vos@student.utwente.nl'),
          ('Sander', 's.t.tenbrinke@student.utwente.nl'), ('Luc', 'l.w.l.jansen@student.utwente.nl')]
