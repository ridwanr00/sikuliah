"""Model materi pembelajaran (FR-05)."""

from pathlib import Path

from django.core.exceptions import ValidationError
from django.db import models

from apps.common import upload_path


def material_file_path(instance, filename):
    return upload_path("materials", filename)


class Material(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="materials",
        verbose_name="mata kuliah",
    )
    title = models.CharField("judul", max_length=200)
    meeting_no = models.PositiveSmallIntegerField(
        "pertemuan ke-",
        default=1,
        choices=[(i, f"Pertemuan {i}") for i in range(1, 17)],
    )
    description = models.TextField("deskripsi", blank=True)
    file = models.FileField("berkas", upload_to=material_file_path, blank=True)
    external_url = models.URLField("tautan eksternal", blank=True)
    is_required = models.BooleanField("wajib dibaca", default=False)
    uploaded_at = models.DateTimeField("diunggah pada", auto_now_add=True)

    class Meta:
        verbose_name = "materi"
        verbose_name_plural = "materi"
        ordering = ["meeting_no", "title"]

    def __str__(self):
        return f"Pertemuan {self.meeting_no} — {self.title}"

    def clean(self):
        if not self.file and not self.external_url:
            raise ValidationError("Isi salah satu: unggah berkas atau tautan eksternal.")

    @property
    def filename(self) -> str:
        return Path(self.file.name).name if self.file else ""

    @property
    def size_display(self) -> str:
        if not self.file:
            return ""
        try:
            size = self.file.size
        except OSError:
            return ""
        if size >= 1024 * 1024:
            return f"{size / (1024 * 1024):.1f} MB"
        return f"{max(size // 1024, 1)} KB"
