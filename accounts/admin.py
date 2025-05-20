from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = BaseUserAdmin.fieldsets + (
        (
            "Additional Info",
            {"fields": ("phone",)},
        ),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        (
            "Additional Info",
            {
                "fields": (
                    "email",
                    "phone",
                )
            },
        ),
    )
    list_display = (
        "username",
        "email",
        "phone",
        "is_staff",
        "is_superuser",
    )
