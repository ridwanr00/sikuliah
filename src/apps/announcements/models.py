"""Model pengumuman mata kuliah (FR-09)."""

from django.db import models


class Announcement(models.Model):
    course = models.ForeignKey(
        "courses.Course",
        on_delete=models.CASCADE,
        related_name="announcements",
        verbose_name="mata kuliah",
    )
    title = models.CharField("judul", max_length=200)
    body = models.TextField("isi")
    published_at = models.DateTimeField("diterbitkan pada", auto_now_add=True)

    class Meta:
        verbose_name = "pengumuman"
        verbose_name_plural = "pengumuman"
        ordering = ["-published_at"]

    def __str__(self):
        return self.title
