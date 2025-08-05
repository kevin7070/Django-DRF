from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Company, CompanyAddress, CompanyRole, User


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
