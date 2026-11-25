"""Formulir pengelolaan pengguna (FR-02), dipakai di panel admin."""

from django.contrib.auth.forms import UserCreationForm

from .models import User


class UserCreateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "identity_number", "role")


class UserUpdateForm(UserCreationForm):
    class Meta:
        model = User
        fields = ("email", "full_name", "identity_number", "role")
