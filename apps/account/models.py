from django.conf import settings
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models

from apps.account.constants import USER_PERMISSION_DEFAULT
from apps.utils.base_model import UUIDBaseModel
from apps.utils.uploads import upload_path


def default_role_permissions():
    """
    Return a copy of the default role permissions.

    :return: copy of USER_PERMISSION_DEFAULT
    :rtype: dict
    """
    return USER_PERMISSION_DEFAULT.copy()


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password, **extra_fields):
        """
        Creates a new user with the given username, email and password.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str): The password of the user.
            **extra_fields (dict): Additional fields for the user.

        Returns:
            User: The newly created user.

        Raises:
            ValueError: If username, email or password is not provided.
        """
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
        """
        Creates a new superuser with the given username, email and password.

        Args:
            username (str): The username of the user.
            email (str): The email of the user.
            password (str): The password of the user.
            **extra_fields (dict): Additional fields for the user.

        Returns:
            User: The newly created superuser.

        Raises:
            ValueError: If is_staff or is_superuser is not True in extra_fields.
        """
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser must have is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser must have is_superuser=True.")

        return self.create_user(username, email, password, **extra_fields)


class User(UUIDBaseModel, AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)  # unique
    mobile = models.CharField(
        max_length=12, null=True, blank=True
    )  # todo: api validation
    profile_picture = models.ImageField(
        upload_to=upload_path(use_day=False), null=True, blank=True
    )
    # Many-to-many companies via membership payload
    companies = models.ManyToManyField(
        "Company",
        through="CompanyMembership",
        through_fields=("user", "company"),
        related_name="users",
        blank=True,
    )

    # Custom user manager
    objects = UserManager()

    # username is a required field
    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["username"]

    def __str__(self):
        return self.username


# Company membership through model
class CompanyMembership(UUIDBaseModel):
    """User ↔ Company membership with role and status payload."""

    PENDING = "pending"
    ACTIVE = "active"
    INACTIVE = "inactive"
    STATUS_CHOICES = [
        (PENDING, "Pending"),
        (ACTIVE, "Active"),
        (INACTIVE, "Inactive"),
    ]

    user = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    company = models.ForeignKey(
        "Company",
        on_delete=models.CASCADE,
        related_name="memberships",
    )
    role = models.ForeignKey(
        "CompanyRole",
        on_delete=models.SET_NULL,
        null=True,
        blank=True,
        related_name="members",
    )

    status = models.CharField(max_length=16, choices=STATUS_CHOICES, default=ACTIVE)
    is_primary = models.BooleanField(default=False)
    joined_at = models.DateTimeField(auto_now_add=True)
    invited_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="invitations_sent",
    )

    class Meta:
        unique_together = [("user", "company")]
        indexes = [models.Index(fields=["user", "company"])]

    def __str__(self):
        role_name = self.role.name if self.role else "no-role"
        return f"{self.user} @ {self.company} ({role_name})"

    def has_perm(self, module: str, action: str) -> bool:
        return self.role.has_perm(module, action) if self.role else False


class Company(UUIDBaseModel):
    name = models.CharField(max_length=100)
    verification_document = models.FileField(
        upload_to=upload_path(use_day=False), blank=True, null=True
    )
    verified_at = models.DateTimeField(null=True, blank=True)
    verified_by = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        null=True,
        blank=True,
        on_delete=models.SET_NULL,
        related_name="verified_companies",
    )

    @property
    def is_verified(self) -> bool:
        return self.verified_at is not None

    def __str__(self):
        return self.name


class CompanyAddress(UUIDBaseModel):
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
        """
        Returns a string representation of the full address of the company address.

        The full address is a string representation of the address, apt_suite, city, province, postal_code, and country.
        The parts are concatenated using commas and any empty or None parts are filtered out.

        Returns:
            str: A string representation of the full address.
        """
        parts = [self.address]
        if self.apt_suite:
            parts.append(self.apt_suite)
        parts += [self.city, self.province, self.postal_code, self.country]
        return ", ".join(filter(None, parts))

    def __str__(self):
        return self.full_address


class CompanyRole(UUIDBaseModel):
    company = models.ForeignKey(Company, on_delete=models.CASCADE, related_name="roles")
    name = models.CharField(max_length=50)  # e.g., admin, user, vip
    permissions = models.JSONField(default=default_role_permissions)
    is_protected = models.BooleanField(default=False)

    def has_perm(self, module: str, action: str) -> bool:
        """
        Check if the given module and action are allowed for the user's company role.

        Args:
            module (str): The module to check permissions for.
            action (str): The action to check permissions for.

        Returns:
            bool: True if the module and action are allowed, False otherwise.
        """
        return self.permissions.get(module, {}).get(action, False)

    def __str__(self):
        return f"{self.company.name} - {self.name}"
