"""Panel admin Django untuk pengguna (memenuhi FR-02)."""

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .forms import UserCreateForm
from .models import User


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    add_form = UserCreateForm
    model = User

    list_display = ("full_name", "email", "identity_number", "role", "is_active")
    list_filter = ("role", "is_active")
    search_fields = ("full_name", "email", "identity_number")
    ordering = ("full_name",)
    readonly_fields = ("last_login", "date_joined")

    fieldsets = (
        (None, {"fields": ("email", "password")}),
        ("Identitas", {"fields": ("full_name", "identity_number", "role")}),
        (
            "Izin",
            {"fields": ("is_active", "is_staff", "is_superuser", "groups", "user_permissions")},
        ),
        ("Riwayat", {"fields": ("last_login", "date_joined")}),
    )
    add_fieldsets = (
        (
            None,
            {
                "classes": ("wide",),
                "fields": (
                    "email",
                    "full_name",
                    "identity_number",
                    "role",
                    "password1",
                    "password2",
                ),
            },
        ),
    )
