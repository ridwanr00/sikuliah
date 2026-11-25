"""Utilitas bersama untuk validasi berkas dan format tampilan."""

from pathlib import Path

from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError


def get_extension(filename: str) -> str:
    return Path(filename).suffix.lower().lstrip(".")


def validate_upload(file_obj) -> None:
    """Validasi ekstensi dan ukuran berkas (BR-05).

    Dipakai oleh form materi, form pengumpulan, dan lampiran tugas sehingga aturannya
    konsisten di semua titik unggah.
    """
    if not file_obj:
        return

    extension = get_extension(file_obj.name)
    if extension not in settings.ALLOWED_UPLOAD_EXTENSIONS:
        allowed = ", ".join(sorted(settings.ALLOWED_UPLOAD_EXTENSIONS))
        raise ValidationError(f"Format .{extension or '?'} tidak diizinkan. Gunakan: {allowed}.")

    if file_obj.size > settings.MAX_UPLOAD_SIZE_BYTES:
        raise ValidationError(
            f"Ukuran berkas maksimum {settings.MAX_UPLOAD_SIZE_MB} MB. "
            f"Berkas Anda {file_obj.size / (1024 * 1024):.1f} MB."
        )

    if file_obj.size == 0:
        raise ValidationError("Berkas kosong (0 byte). Pilih berkas lain.")


def upload_path(prefix: str, filename: str) -> str:
    """Nama berkas acak + ekstensi asli (BR: nama asli disimpan di kolom terpisah)."""
    from datetime import date
    from uuid import uuid4

    suffix = Path(filename).suffix.lower()
    return f"{prefix}/{date.today():%Y/%m}/{uuid4().hex}{suffix}"


def grade_distribution(scores):
    """Distribusi nilai per rentang 20 poin (FR-10)."""
    buckets = [0, 0, 0, 0, 0]
    labels = ["0–20", "21–40", "41–60", "61–80", "81–100"]
    for score in scores:
        if score is None:
            continue
        index = min(int(score) // 20, 4)
        buckets[index] += 1
    return {"labels": labels, "values": buckets}


class BootstrapFormMixin:
    """Tambahkan kelas Bootstrap pada widget agar formulir tampil konsisten."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        for field in self.fields.values():
            widget = field.widget
            if isinstance(widget, forms.CheckboxInput):
                widget.attrs.setdefault("class", "form-check-input")
            elif isinstance(widget, forms.Select):
                widget.attrs.setdefault("class", "form-select")
            elif isinstance(widget, forms.FileInput):
                widget.attrs.setdefault("class", "form-control")
            else:
                widget.attrs.setdefault("class", "form-control")
