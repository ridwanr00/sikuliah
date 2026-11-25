"""Formulir materi dengan validasi berkas (FR-05, BR-05)."""

from django import forms

from apps.common import BootstrapFormMixin, get_extension, validate_upload

from .models import Material


class MaterialForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Material
        fields = ("title", "meeting_no", "description", "file", "external_url", "is_required")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 3}),
            "title": forms.TextInput(attrs={"placeholder": "Contoh: Pemodelan Use Case"}),
            "external_url": forms.URLInput(attrs={"placeholder": "https://..."}),
        }

    def clean_file(self):
        file_obj = self.cleaned_data.get("file")
        validate_upload(file_obj)
        return file_obj

    def clean(self):
        cleaned = super().clean()
        file_obj = cleaned.get("file")
        url = cleaned.get("external_url")

        # Saat mengubah materi tanpa mengganti berkas, berkas lama tetap dipakai.
        # Aturan "wajib salah satu" ditegakkan oleh Material.clean() agar pesan tidak ganda.
        if file_obj and url:
            raise forms.ValidationError(
                "Pilih salah satu saja: unggah berkas atau tautan eksternal."
            )
        return cleaned

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Judul minimal 3 karakter.")
        return title

    @property
    def uploaded_extension(self) -> str:
        file_obj = self.cleaned_data.get("file") if hasattr(self, "cleaned_data") else None
        return get_extension(file_obj.name) if file_obj else ""
