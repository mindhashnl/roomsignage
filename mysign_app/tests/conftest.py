# Make sure that the helper method asserts are handled as pytest asserts
import pytest

pytest.register_assert_rewrite("mysign_app.tests.routes.authentication_helpers")
pytest.register_assert_rewrite("mysign_app.tests.routes.form_helpers")


@pytest.fixture(autouse=True)
def email_backend_setup(settings):
    # Keep mailing local during test
    settings.EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
