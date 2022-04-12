from django.contrib import admin

from django.contrib.auth.admin import UserAdmin
from users.models import User


@admin.register(User)
class CustomUserAdmin(UserAdmin):

    list_display = (
        "user_id",
        "username",
        "email",
        "is_staff",
        "is_superuser",
    )
