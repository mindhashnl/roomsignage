import os
from datetime import date

from django.conf import settings
import pytest
import chromedriver_binary
from selenium import webdriver

DEFAULT_ENGINE = 'django.db.backends.postgresql_psycopg2'

HOMEPAGE = 'http://localhost:8000'
TODAY = date.today()

@pytest.fixture(scope="module")
def driver():
    driver = webdriver.Chrome()
    yield driver
    driver.quit()

@pytest.fixture(scope='session')
def test_django_db_setup():
    settings.DATABASES['default'] = {
        'ENGINE': os.environ.get("DB_ENGINE", DEFAULT_ENGINE),
        'HOST': os.environ["DB_HOST"],
        'NAME': os.environ["DB_NAME"],  # my dedicated test database (!)
        'PORT': os.environ["DB_PORT"],
        'USER': os.environ["DB_USER"],
        'PASSWORD': os.environ["DB_PASSWORD"],
    }

def test_loggedout_homepage(driver):
    driver.get(HOMEPAGE)
    expected = "PyBites Code Challenges | Hone Your Python Skills"
    assert driver.title == expected
