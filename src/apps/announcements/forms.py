"""Formulir pengumuman (FR-09)."""

from django import forms

from apps.common import BootstrapFormMixin

from .models import Announcement


class AnnouncementForm(BootstrapFormMixin, forms.ModelForm):
    class Meta:
        model = Announcement
        fields = ("title", "body")
        widgets = {"body": forms.Textarea(attrs={"rows": 4})}

    def clean_title(self):
        title = self.cleaned_data["title"].strip()
        if len(title) < 3:
            raise forms.ValidationError("Judul minimal 3 karakter.")
        return title
