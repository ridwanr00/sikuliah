"""Dasbor dan statistik (FR-10)."""

from django.contrib.auth.mixins import LoginRequiredMixin
from django.db.models import Avg, Count, Q
from django.utils import timezone
from django.views.generic import TemplateView

from apps.assignments.models import Assignment, Submission
from apps.common import grade_distribution
from apps.courses.models import Course, Enrollment


class DashboardView(LoginRequiredMixin, TemplateView):
    def get_template_names(self):
        role = self.request.user.role
        if role == "dosen":
            return ["dashboard/dosen.html"]
        if role == "admin":
            return ["dashboard/admin.html"]
        return ["dashboard/mahasiswa.html"]

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        if user.is_mahasiswa:
            context.update(self.mahasiswa_context(user))
        elif user.is_dosen:
            context.update(self.lecturer_context(user))
        else:
            context.update(self.admin_context())
        return context

    # --- Mahasiswa ---------------------------------------------------------
    def mahasiswa_context(self, user):
        enrollments = Enrollment.objects.filter(
            student=user, status=Enrollment.Status.ACTIVE
        ).select_related("course", "course__lecturer")
        courses = [enrollment.course for enrollment in enrollments]
        submissions = {
            submission.assignment_id: submission
            for submission in Submission.objects.filter(student=user)
        }

        deadlines = (
            Assignment.objects.filter(course__in=courses, due_at__gte=timezone.now())
            .select_related("course")
            .order_by("due_at")[:5]
        )
        pending = [
            assignment
            for assignment in deadlines
            if assignment.id not in submissions or submissions[assignment.id].is_graded is False
        ]

        graded = [s for s in submissions.values() if s.is_graded]
        average = round(sum(s.score for s in graded) / len(graded), 1) if graded else None

        return {
            "courses": courses,
            "deadlines": deadlines,
            "pending_count": len(pending),
            "submission_count": len(submissions),
            "graded_count": len(graded),
            "average_score": average,
            "my_submissions": submissions,
        }

    # --- Dosen -------------------------------------------------------------
    def lecturer_context(self, user):
        courses = (
            Course.objects.filter(lecturer=user)
            .annotate(
                student_count=Count(
                    "enrollments",
                    filter=Q(enrollments__status=Enrollment.Status.ACTIVE),
                    distinct=True,
                ),
                assignment_count=Count("assignments", distinct=True),
            )
            .order_by("code")
        )
        course_ids = [course.id for course in courses]
        assignments = Assignment.objects.filter(course_id__in=course_ids)

        participant_pairs = sum(course.student_count for course in courses)
        # Target pengumpulan = jumlah peserta x jumlah tugas pada mata kuliah itu sendiri.
        expected = sum(
            course.student_count * course.assignment_count for course in courses
        )
        submitted = Submission.objects.filter(assignment__in=assignments).count()
        scored = Submission.objects.filter(assignment__in=assignments, score__isnull=False)
        average = scored.aggregate(value=Avg("score"))["value"]

        return {
            "courses": courses,
            "course_count": courses.count(),
            "student_count": participant_pairs,
            "assignment_count": assignments.count(),
            "submitted_count": submitted,
            "expected_submissions": expected,
            "submission_rate": round(submitted / expected * 100) if expected else 0,
            "graded_count": scored.count(),
            "average_score": round(average, 1) if average is not None else None,
            "upcoming": assignments.filter(due_at__gte=timezone.now())
            .select_related("course")
            .order_by("due_at")[:5],
            "distribution": grade_distribution(scored.values_list("score", flat=True)),
        }

    # --- Admin -------------------------------------------------------------
    def admin_context(self):
        courses = (
            Course.objects.select_related("lecturer")
            .annotate(
                student_count=Count(
                    "enrollments",
                    filter=Q(enrollments__status=Enrollment.Status.ACTIVE),
                    distinct=True,
                )
            )
            .order_by("code")
        )
        assignments = Assignment.objects.all()
        expected = (
            Enrollment.objects.filter(status=Enrollment.Status.ACTIVE).count() * assignments.count()
        )
        submitted = Submission.objects.count()
        scored = Submission.objects.filter(score__isnull=False)
        average = scored.aggregate(value=Avg("score"))["value"]

        return {
            "courses": courses,
            "course_count": courses.count(),
            "student_count": Enrollment.objects.filter(status=Enrollment.Status.ACTIVE).count(),
            "assignment_count": assignments.count(),
            "submitted_count": submitted,
            "expected_submissions": expected,
            "submission_rate": round(submitted / expected * 100) if expected else 0,
            "graded_count": scored.count(),
            "average_score": round(average, 1) if average is not None else None,
            "distribution": grade_distribution(scored.values_list("score", flat=True)),
        }
