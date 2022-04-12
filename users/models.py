import uuid
from django.utils import timezone
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)


class UserManager(BaseUserManager):
    def create_user(self, email, password, **otherfields):
        """
        Create a user and return username, email and password
        """

        if not email:
            raise ValueError("Email must not be an empty string")

        user = self.model(email=self.normalize_email(email), **otherfields)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, email, password, **other_fields):
        """
        Create user with super admin permissions
        """
        if email is None:
            raise TypeError("Super Users must have an email")

        if password is None:
            raise TypeError("Super Users must have a password")

        other_fields.setdefault("is_superuser", True)

        return self.create_user(email, password, **other_fields)

    def has_perm(self, perm, obj=None):
        return self.is_superuser

    def has_module_perms(self, app_label):
        return self.is_superuser


class User(AbstractBaseUser, PermissionsMixin):

    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, unique=True)
    username = models.CharField(max_length=255)
    email = models.EmailField(
        verbose_name="email address",
        max_length=255,
        unique=True,
        error_messages={"unique": "This email has already been registered."},
    )
    password = models.CharField(max_length=255)
    last_login = models.DateTimeField(null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=True)
    is_superuser = models.BooleanField(default=False)
    created = models.DateTimeField(default=timezone.now)
    updated = models.DateTimeField(null=True)

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["password"]
    objects = UserManager()

    def __str__(self):
        return (self.user_id, self.email)

    class Meta:
        db_table = "users"
        ordering = ["-created"]
