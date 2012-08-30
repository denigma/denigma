from django.contrib import admin

import reversion

from pinax.apps.account.models import Account, PasswordReset


class AccountAdmin(reversion.VersionAdmin):
    pass


class PasswordResetAdmin(admin.ModelAdmin):
    list_display = ["user", "temp_key", "timestamp", "reset"]


admin.site.register(Account, AccountAdmin)
admin.site.register(PasswordReset, PasswordResetAdmin)
