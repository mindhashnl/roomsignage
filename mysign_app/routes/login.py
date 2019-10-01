from django.conf import settings
from django.contrib import messages
from django.contrib.auth import logout as auth_logout
from django.contrib.auth.views import logout_then_login, LoginView
from django.shortcuts import redirect
from django.urls import reverse


class Login(LoginView):
    redirect_authenticated_user = True

    def get_success_url(self):
        url = self.get_redirect_url()  # URL where user originated from
        if url:
            return url
        elif self.request.user.is_admin:
            return reverse('admin_door_devices')
        elif self.request.user.company:
            return reverse('company_index')
        elif self.request.user.is_staff:
            return '/django_admin'
        else:
            messages.error(self.request, 'We cannot idenitify the usertype of this user. '
                                         'Please check that this user is configured as staff, admin or company user.')
            auth_logout(self.request)
            redirect(settings.LOGIN_URL)


def logout(request):
    messages.success(request, 'You were successfully logged-out.')
    return logout_then_login(request)
