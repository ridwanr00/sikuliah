from django.contrib import admin

from .models import Material


@admin.register(Material)
class MaterialAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "meeting_no", "is_required", "uploaded_at")
    list_filter = ("is_required", "course")
    search_fields = ("title", "course__code", "course__name")
    autocomplete_fields = ("course",)
