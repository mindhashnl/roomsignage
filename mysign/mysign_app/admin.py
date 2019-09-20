from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django_admin_row_actions import AdminRowActionsMixin

from .models import Company, DoorDevice, User

admin.site.register(User, UserAdmin)


class DoorDeviceInline(admin.TabularInline):
    model = DoorDevice
    exclude = ('secret',)
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    inlines = [DoorDeviceInline]


admin.site.register(Company, CompanyAdmin)


class DoorDeviceAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    exclude = ('secret',)
    list_display = ('id', 'company')


admin.site.register(DoorDevice, DoorDeviceAdmin)
