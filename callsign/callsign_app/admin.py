from django.contrib import admin

from .models import Company, DoorDevice

admin.site.register(Company)


class DoorDeviceAdmin(admin.ModelAdmin):
    readonly_fields = ('pairing_code', 'pairing_code_expire_at')
    exclude = ('secret',)


admin.site.register(DoorDevice, DoorDeviceAdmin)
