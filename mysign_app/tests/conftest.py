# Make sure that the helper method asserts are handled as pytest asserts
import pytest

pytest.register_assert_rewrite("mysign_app.tests.routes.authentication_helpers")
pytest.register_assert_rewrite("mysign_app.tests.routes.form_helpers")
