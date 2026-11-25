"""Model pengguna dan peran (FR-01, FR-02)."""

from django.contrib.auth.models import AbstractUser, BaseUserManager
from django.db import models


class Role(models.TextChoices):
    ADMIN = "admin", "Admin"
    DOSEN = "dosen", "Dosen"
    MAHASISWA = "mahasiswa", "Mahasiswa"


class UserManager(BaseUserManager):
    use_in_migrations = True

    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("Surel wajib diisi")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)
        extra_fields.setdefault("role", Role.ADMIN)
        extra_fields.setdefault("full_name", "Administrator")
        extra_fields.setdefault("identity_number", "ADMIN-000")
        return self.create_user(email, password, **extra_fields)


class User(AbstractUser):
    """Pengguna dengan peran tunggal; surel dipakai sebagai nama pengguna."""

    username = None
    email = models.EmailField("surel", unique=True)
    full_name = models.CharField("nama lengkap", max_length=120)
    identity_number = models.CharField("NIM/NIDN", max_length=20, unique=True)
    role = models.CharField("peran", max_length=10, choices=Role.choices, default=Role.MAHASISWA)

    objects = UserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = ["full_name", "identity_number"]

    class Meta:
        verbose_name = "pengguna"
        verbose_name_plural = "pengguna"
        ordering = ["full_name"]

    def __str__(self):
        return f"{self.full_name} ({self.get_role_display()})"

    @property
    def is_admin(self):
        return self.role == Role.ADMIN

    @property
    def is_dosen(self):
        return self.role == Role.DOSEN

    @property
    def is_mahasiswa(self):
        return self.role == Role.MAHASISWA
