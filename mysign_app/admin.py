from django.contrib import admin
from django_use_email_as_username.admin import BaseUserAdmin

from .models import Company, DoorDevice, User


class CustomUserAdmin(BaseUserAdmin):
    fieldsets = ((None, {'fields': ('company',)}),
                 ) + BaseUserAdmin.fieldsets


admin.site.register(User, CustomUserAdmin)


class DoorDeviceInline(admin.TabularInline):
    model = DoorDevice
    exclude = ('secret',)
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    inlines = [DoorDeviceInline]


admin.site.register(Company, CompanyAdmin)


class DoorDeviceAdmin(admin.ModelAdmin):
    exclude = ('secret',)
    list_display = ('id', 'company')


admin.site.register(DoorDevice, DoorDeviceAdmin)
