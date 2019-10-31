# Make sure that the helper method asserts are handled as pytest asserts
import pytest

pytest.register_assert_rewrite("mysign_app.tests.routes.authentication_helpers")
pytest.register_assert_rewrite("mysign_app.tests.routes.form_helpers")


@pytest.fixture(autouse=True)
def _email_backend_setup(settings):
    # Keep mailing local during test
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'

    # Set websockets to memory store
    settings.CHANNEL_LAYERS = {"default": {
        "BACKEND": "channels.layers.InMemoryChannelLayer"
    }}


@pytest.fixture()
def chrome_options(chrome_options):
    # https://stackoverflow.com/questions/50642308/webdriverexception-unknown-error-devtoolsactiveport-file-doesnt-exist-while-t
    # chrome_options.add_argument('disable-dev-shm-usage')
    # chrome_options.add_argument('no-sandbox')
    # chrome_options.add_argument('headless')
    # chrome_options.add_argument('window-size=1920x1080')
    return chrome_options


@pytest.fixture()
def firefox_options(firefox_options):
    firefox_options.add_argument('--headless')
    firefox_options.add_argument("--width=1920")
    firefox_options.add_argument("--height=1080")
    return firefox_options
