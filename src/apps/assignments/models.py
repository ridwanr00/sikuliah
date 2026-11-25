"""Model tugas dan pengumpulan (FR-06, FR-07, FR-08)."""

from pathlib import Path

from django.conf import settings
from django.core.exceptions import ValidationError
from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.utils import timezone

from apps.common import upload_path


def submission_file_path(instance, filename):
    return upload_path("submissions", filename)


class Assignment(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="assignments",
        verbose_name="mata kuliah",
    )
    title = models.CharField("judul tugas", max_length=200)
    description = models.TextField("deskripsi")
    due_at = models.DateTimeField("tenggat")
    max_score = models.PositiveSmallIntegerField(
        "nilai maksimum",
        default=100,
        validators=[MinValueValidator(1), MaxValueValidator(100)],
    )
    attachment = models.FileField("lampiran", upload_to="assignments/", blank=True)
    created_at = models.DateTimeField("dibuat pada", auto_now_add=True)

    class Meta:
        verbose_name = "tugas"
        verbose_name_plural = "tugas"
        ordering = ["due_at"]

    def __str__(self):
        return f"{self.course.code} — {self.title}"

    @property
    def is_past_due(self) -> bool:
        return timezone.now() > self.due_at

    @property
    def status_label(self) -> str:
        return "Lewat tenggat" if self.is_past_due else "Aktif"


class Submission(models.Model):
    assignment = models.ForeignKey(
        Assignment,
        on_delete=models.CASCADE,
        related_name="submissions",
        verbose_name="tugas",
    )
    student = models.ForeignKey(
        settings.AUTH_USER_MODEL,
        on_delete=models.CASCADE,
        related_name="submissions",
        limit_choices_to={"role": "mahasiswa"},
        verbose_name="mahasiswa",
    )
    file = models.FileField("berkas jawaban", upload_to=submission_file_path)
    original_filename = models.CharField("nama berkas asli", max_length=255)
    submitted_at = models.DateTimeField("waktu kumpul", default=timezone.now)
    score = models.PositiveSmallIntegerField(
        "nilai",
        null=True,
        blank=True,
        validators=[MinValueValidator(0), MaxValueValidator(100)],
    )
    feedback = models.TextField("umpan balik", blank=True)
    graded_at = models.DateTimeField("dinilai pada", null=True, blank=True)

    class Meta:
        verbose_name = "pengumpulan"
        verbose_name_plural = "pengumpulan"
        ordering = ["-submitted_at"]
        constraints = [
            models.UniqueConstraint(
                fields=["assignment", "student"], name="unique_submission_per_student"
            )
        ]

    def __str__(self):
        return f"{self.student.full_name} → {self.assignment.title}"

    def clean(self):
        super().clean()
        if self.score is not None and self.score > self.assignment.max_score:
            raise ValidationError(
                {"score": f"Nilai maksimum tugas ini {self.assignment.max_score}."}
            )

    def save(self, *args, **kwargs):
        # BR-03: nilai tidak boleh melebihi nilai maksimum tugas, termasuk lewat admin.
        if self.score is not None and self.score > self.assignment.max_score:
            raise ValidationError(
                {"score": f"Nilai maksimum tugas ini {self.assignment.max_score}."}
            )
        super().save(*args, **kwargs)

    @property
    def is_graded(self) -> bool:
        return self.score is not None

    @property
    def filename(self) -> str:
        return Path(self.file.name).name

    @property
    def status_label(self) -> str:
        return "Dinilai" if self.is_graded else "Terkumpul"
