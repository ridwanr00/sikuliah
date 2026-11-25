from django.contrib import admin

from .models import Announcement


@admin.register(Announcement)
class AnnouncementAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "published_at")
    list_filter = ("course",)
    search_fields = ("title", "course__code")
    autocomplete_fields = ("course",)
