from django.contrib import admin
from django_admin_row_actions import AdminRowActionsMixin

from .models import Company, DoorDevice


class DoorDeviceInline(admin.TabularInline):
    model = DoorDevice
    exclude = ('secret',)
    extra = 0


class CompanyAdmin(admin.ModelAdmin):
    inlines = [DoorDeviceInline]


admin.site.register(Company, CompanyAdmin)


class DoorDeviceAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    exclude = ('secret',)
    list_display = ('id', 'room_number', 'company')


admin.site.register(DoorDevice, DoorDeviceAdmin)
