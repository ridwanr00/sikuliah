"""Model mata kuliah dan pendaftaran (FR-03, FR-04)."""

from django.conf import settings
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models


class Course(models.Model):
    class Semester(models.TextChoices):
        GANJIL = "Ganjil", "Ganjil"
        GENAP = "Genap", "Genap"

    code = models.CharField("kode", max_length=10, unique=True)
    name = models.CharField("nama mata kuliah", max_length=150)
    credits = models.PositiveSmallIntegerField(
        "SKS", default=3, validators=[MinValueValidator(1), MaxValueValidator(6)]
    )
    semester = models.CharField(
        "semester", max_length=10, choices=Semester.choices, default=Semester.GANJIL
    )
    academic_year = models.CharField("tahun ajaran", max_length=9, default="2026/2027")
    description = models.TextField("deskripsi", blank=True)
    is_archived = models.BooleanField("diarsipkan", default=False)
    lecturer = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.PROTECT,
        related_name="courses_taught",
        limit_choices_to={"role": "dosen"},
        verbose_name="dosen pengampu",
    )

    class Meta:
        verbose_name = "mata kuliah"
        verbose_name_plural = "mata kuliah"
        ordering = ["code"]

    def __str__(self):
        return f"{self.code} — {self.name}"

    def save(self, *args, **kwargs):
        self.code = self.code.strip().upper()
        super().save(*args, **kwargs)

    def can_manage(self, user) -> bool:
        return user.is_authenticated and (
            user.role == "admin" or (user.role == "dosen" and self.lecturer_id == user.id)
        )

    def is_participant(self, user) -> bool:
        if not user.is_authenticated or user.role != "mahasiswa":
            return False
        return self.enrollments.filter(student=user, status=Enrollment.Status.ACTIVE).exists()

    def can_access(self, user) -> bool:
        return self.can_manage(user) or self.is_participant(user)


class Enrollment(models.Model):
    class Status(models.TextChoices):
        ACTIVE = "active", "Aktif"
        DROPPED = "dropped", "Dibatalkan"

    course = models.ForeignKey(
        Course, on_delete=models.CASCADE, related_name="enrollments", verbose_name="mata kuliah"
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="enrollments",
        limit_choices_to={"role": "mahasiswa"},
        verbose_name="mahasiswa",
    )
    enrolled_at = models.DateTimeField("waktu daftar", auto_now_add=True)
    status = models.CharField(
        "status", max_length=10, choices=Status.choices, default=Status.ACTIVE
    )

    class Meta:
        verbose_name = "pendaftaran"
        verbose_name_plural = "pendaftaran"
        constraints = [
            models.UniqueConstraint(fields=["course", "student"], name="unique_enrollment")
        ]

    def __str__(self):
        return f"{self.student.full_name} → {self.course.code}"
