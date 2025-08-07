from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.account.constants import USER_PERMISSION_DEFAULT
from apps.utils.base_model import UUIDBaseModel, UUIDTimestampModel


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        if not password:
            raise ValueError("Password is required")

        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(UUIDBaseModel, AbstractUser):
    company = models.ForeignKey(
        "Company",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    company_role = models.ForeignKey(
        "CompanyRole",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="users",
    )
    email = models.EmailField(unique=True, null=False, blank=False)  # unique
    phone = models.CharField(max_length=12, null=True, blank=True)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="user/profile_picture/", null=True, blank=True
    )

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


class Company(UUIDTimestampModel):
    name = models.CharField(max_length=100)
    verification_document = models.FileField(
        upload_to="company/verification_document/", blank=True, null=True
    )
    is_verified = models.BooleanField(default=False)
    verified = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_companies",
    )

    def __str__(self):
        return self.name


class CompanyAddress(UUIDTimestampModel):
    company = models.ForeignKey(
        Company, on_delete=models.CASCADE, related_name="addresses"
    )

    address = models.CharField(max_length=255)
    apt_suite = models.CharField(max_length=255, blank=True, null=True)
    city = models.CharField(max_length=255)
    province = models.CharField(max_length=255)
    postal_code = models.CharField(max_length=255)
    country = models.CharField(max_length=255)

    is_mailing_address = models.BooleanField(default=False)

    @property
    def full_address(self):
        parts = [self.address]
        if self.apt_suite:
            parts.append(self.apt_suite)
        parts += [self.city, self.province, self.postal_code, self.country]
        return ", ".join(filter(None, parts))

    def __str__(self):
        return self.full_address


class CompanyRole(UUIDTimestampModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=50)  # e.g., admin, user, vip
    permissions = models.JSONField(default=lambda: USER_PERMISSION_DEFAULT.copy())
    is_protected = models.BooleanField(default=False)

    def has_perm(self, module: str, action: str) -> bool:
        return self.permissions.get(module, {}).get(action, False)

    # usage
    # check if user.company_role and user.company_role.has_perm("product", "edit")

    def __str__(self):
        return f"{self.company.name} - {self.name}"
