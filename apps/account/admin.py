from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Company, CompanyAddress, CompanyRole, User


# Register your models here.
@admin.register(User)
class UserAdmin(BaseUserAdmin):
    fieldsets = (
        (None, {"fields": ("email", "username", "password")}),
        (
            "Permissions",
            {
                "fields": (
                    "is_active",
                    "is_staff",
                    "is_superuser",
                    "groups",
                    "user_permissions",
                )
            },
        ),
        ("Important dates", {"fields": ("last_login", "date_joined")}),
        (
            "Additional Info",
            {
                "fields": (
                    "mobile",
                    "profile_picture",
                    "company",
                    "company_role",
                )
            },
        ),
    )

    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "username",
                    "mobile",
                    "profile_picture",
                    "company",
                    "company_role",
                    "password1",
                    "password2",
                    "is_staff",
                    "is_active",
                ),
            },
        ),
    )

    list_display = ("email", "username", "is_staff", "is_superuser")
    search_fields = (
        "email",
        "username",
    )
    ordering = ("email",)


@admin.register(Company)
class CompanyAdmin(admin.ModelAdmin):
    list_display = (
        "name",
        "is_verified",
        "verified",
        "verified_by",
        "has_mailing_address",
    )
    list_filter = ("is_verified", "verified_by")
    search_fields = ("name",)
    readonly_fields = ("verified", "verified_by")

    def has_mailing_address(self, obj):
        return obj.addresses.filter(is_mailing_address=True).exists()

    has_mailing_address.boolean = True
    has_mailing_address.short_description = "Mailing Address?"


@admin.register(CompanyAddress)
class CompanyAddressAdmin(admin.ModelAdmin):
    list_display = (
        "company",
        "address",
        "apt_suite",
        "city",
        "province",
        "postal_code",
        "country",
        "is_mailing_address",
    )
    list_filter = (
        "company",
        "city",
        "province",
        "country",
        "is_mailing_address",
    )
    search_fields = (
        "address",
        "apt_suite",
        "city",
        "postal_code",
    )


@admin.register(CompanyRole)
class CompanyRoleAdmin(admin.ModelAdmin):
    list_display = ("company", "name")
    search_fields = ("name",)
    list_filter = ("company",)
