"""Formulir tugas, pengumpulan, dan penilaian (FR-06, FR-07, FR-08)."""

from django import forms
from django.utils import timezone

from apps.common import BootstrapFormMixin, validate_upload

from .models import Assignment, Submission


class AssignmentForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Assignment
        fields = ("title", "description", "due_at", "max_score", "attachment")
        widgets = {
            "description": forms.Textarea(attrs={"rows": 5}),
            "due_at": forms.DateTimeInput(
                attrs={"type": "datetime-local"}, format="%Y-%m-%dT%H:%M"
            ),
            "title": forms.TextInput(attrs={"placeholder": "Contoh: Tugas 2 — Analisis Kebutuhan"}),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["due_at"].input_formats = ["%Y-%m-%dT%H:%M"]

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Judul minimal 3 karakter.")
        return title

    def clean_due_at(self):
        due_at = self.cleaned_data["due_at"]
        # BR-04: tenggat tidak boleh di masa lalu.
        if due_at <= timezone.now():
            raise forms.ValidationError(
                "Tenggat harus setelah waktu sekarang. Pilih tanggal dan jam yang akan datang."
            )
        return due_at

    def clean_max_score(self):
        max_score = self.cleaned_data["max_score"]
        if not 1 <= max_score <= 100:
            raise forms.ValidationError("Nilai maksimum harus antara 1 dan 100.")
        return max_score

    def clean_attachment(self):
        attachment = self.cleaned_data.get("attachment")
        validate_upload(attachment)
        return attachment


class SubmissionForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("file",)

    def clean_file(self):
        file_obj = self.cleaned_data.get("file")
        if not file_obj:
            raise forms.ValidationError("Pilih berkas jawaban terlebih dahulu.")
        validate_upload(file_obj)
        return file_obj


class GradeForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Submission
        fields = ("score", "feedback")
        widgets = {"feedback": forms.Textarea(attrs={"rows": 4})}

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields["score"].required = True

    def clean_score(self):
        score = self.cleaned_data["score"]
        max_score = self.instance.assignment.max_score
        if score < 0 or score > max_score:
            raise forms.ValidationError(
                f"Nilai harus antara 0 dan {max_score} (nilai maksimum tugas ini)."
            )
        return score
