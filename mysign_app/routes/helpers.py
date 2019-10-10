from asgiref.sync import async_to_sync
from channels import layers
from django.contrib.auth import REDIRECT_FIELD_NAME
from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth.mixins import AccessMixin
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


class AdminRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.is_admin):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def company_required(*args, **kwargs):
    """
    Decorator for views that checks that the user is logged in and is a company user
    """

    def check_is_company(u):
        if not u.is_authenticated:
            return False
        if not u.company:
            raise PermissionDenied
        return True

    return login_test(check_is_company, *args, **kwargs)


class CompanyRequiredMixin(AccessMixin):
    """Verify that the current user is authenticated."""

    def dispatch(self, request, *args, **kwargs):
        if not (request.user.is_authenticated and request.user.company):
            return self.handle_no_permission()
        return super().dispatch(request, *args, **kwargs)


def refresh_screens(company=None, door_devices=None):
    channel_layer = layers.get_channel_layer()
    if company:
        door_devices = company.door_devices
    for door_device in door_devices:
        async_to_sync(channel_layer.group_send)(
            str(door_device.id),
            {
                "type": "message",
                "action": "refresh",
            },
        )
