from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.core.exceptions import PermissionDenied


def login_test(test, function=None, redirect_field_name=REDIRECT_FIELD_NAME, login_url=None):
    actual_decorator = user_passes_test(
        test,
        login_url=login_url,
        redirect_field_name=redirect_field_name
    )
    if function:
        return actual_decorator(function)
    return actual_decorator


def admin_required(*args, **kwargs):
    """
    Decorator for views that checks that the user is logged in and is an admin
    """

    def check_is_admin(u):
        if not u.is_authenticated:
            return False
        if not u.is_admin:
            raise PermissionDenied
        return True

    return login_test(check_is_admin, *args, **kwargs)


def company_required(*args, **kwargs):
    """
    Decorator for views that checks that the user is logged in and is an company user
    """

    def check_is_company(u):
        if not u.is_authenticated:
            return False
        if not u.company:
            raise PermissionDenied
        return True

    return login_test(check_is_company, *args, **kwargs)
