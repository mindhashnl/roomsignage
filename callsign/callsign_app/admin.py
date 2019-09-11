from django.contrib import admin
from django_admin_row_actions import AdminRowActionsMixin

from .models import Company, DoorDevice

admin.site.register(Company)


class DoorDeviceAdmin(AdminRowActionsMixin, admin.ModelAdmin):
    readonly_fields = ('pairing_code', 'pairing_code_expire_at')
    exclude = ('secret',)

    def get_row_actions(self, obj):
        row_actions = [
            {
                'label': 'Regenerate pairing code',
                'action': 'regenerate_codes',
            }
        ]
        row_actions += super().get_row_actions(obj)
        return row_actions


admin.site.register(DoorDevice, DoorDeviceAdmin)
