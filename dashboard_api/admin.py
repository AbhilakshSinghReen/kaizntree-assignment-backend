from django.contrib import admin

from dashboard_api.models import (
    CustomUser,
)


class CustomUserAdmin(admin.ModelAdmin):
    model = CustomUser


admin.site.register(CustomUser, CustomUserAdmin)
