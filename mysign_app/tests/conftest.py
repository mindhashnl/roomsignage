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


@pytest.fixture
def chrome_options(chrome_options):
    chrome_options.add_argument('headless')
    return chrome_options
