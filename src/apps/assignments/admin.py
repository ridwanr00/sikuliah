from django.contrib import admin

from .models import Assignment, Submission


@admin.register(Assignment)
class AssignmentAdmin(admin.ModelAdmin):
    list_display = ("title", "course", "due_at", "max_score", "status_label")
    list_filter = ("course",)
    search_fields = ("title", "course__code")
    autocomplete_fields = ("course",)


@admin.register(Submission)
class SubmissionAdmin(admin.ModelAdmin):
    list_display = ("student", "assignment", "submitted_at", "score", "graded_at")
    list_filter = ("assignment__course", "assignment")
    search_fields = ("student__full_name", "student__identity_number", "assignment__title")
    autocomplete_fields = ("assignment", "student")
