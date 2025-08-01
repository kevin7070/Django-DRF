from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, username, email, password=None, **extra_fields):
        if not username:
            raise ValueError("Username is required")
        if not email:
            raise ValueError("Email is required")
        email = self.normalize_email(email)
        user = self.model(username=username, email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, username, email, password, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        return self.create_user(username, email, password, **extra_fields)


class User(AbstractUser):
    email = models.EmailField(unique=True, null=False, blank=False)  # unique
    phone = models.CharField(max_length=12, null=True, blank=True)
    mobile = models.CharField(max_length=12, null=True, blank=True)
    profile_picture = models.ImageField(
        upload_to="user/profile_picture/", null=True, blank=True
    )

    objects = UserManager()

    def __str__(self):
        return self.username
