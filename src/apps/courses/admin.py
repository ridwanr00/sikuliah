from django.contrib import admin

from .models import Course, Enrollment


@admin.register(Course)
class CourseAdmin(admin.ModelAdmin):
    list_display = (
        "code",
        "name",
        "credits",
        "semester",
        "academic_year",
        "lecturer",
        "is_archived",
    )
    list_filter = ("semester", "academic_year", "is_archived", "lecturer")
    search_fields = ("code", "name")
    autocomplete_fields = ("lecturer",)


@admin.register(Enrollment)
class EnrollmentAdmin(admin.ModelAdmin):
    list_display = ("course", "student", "status", "enrolled_at")
    list_filter = ("status", "course")
    search_fields = ("student__full_name", "student__identity_number", "course__code")
    autocomplete_fields = ("course", "student")
