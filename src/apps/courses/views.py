"""View daftar/detail mata kuliah dan enrollment (FR-03, FR-04)."""

from django.contrib import messages
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.exceptions import PermissionDenied
from django.db.models import Count, Q
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_POST
from django.views.generic import DetailView, ListView

from apps.accounts.mixins import role_required

from .models import Course, Enrollment


class CourseListView(LoginRequiredMixin, ListView):
    """Daftar mata kuliah sesuai peran, dengan pencarian sederhana (FR-04)."""

    model = Course
    template_name = "courses/course_list.html"
    context_object_name = "courses"
    paginate_by = 20

    def get_queryset(self):
        user = self.request.user
        queryset = Course.objects.select_related("lecturer").annotate(
            student_count=Count(
                "enrollments",
                filter=Q(enrollments__status=Enrollment.Status.ACTIVE),
                distinct=True,
            )
        )
        if user.role == "dosen":
            queryset = queryset.filter(lecturer=user)
        elif user.role == "mahasiswa":
            queryset = queryset.filter(is_archived=False)
        else:
            queryset = queryset.all()

        queryset = queryset.order_by("code")
        query = self.request.GET.get("q", "").strip()
        if query:
            queryset = queryset.filter(Q(code__icontains=query) | Q(name__icontains=query))
        return queryset

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["query"] = self.request.GET.get("q", "").strip()
        if self.request.user.is_mahasiswa:
            context["enrolled_ids"] = set(
                Enrollment.objects.filter(
                    student=self.request.user, status=Enrollment.Status.ACTIVE
                ).values_list("course_id", flat=True)
            )
        return context


class CourseDetailView(LoginRequiredMixin, DetailView):
    model = Course
    template_name = "courses/course_detail.html"
    context_object_name = "course"

    def get_queryset(self):
        return Course.objects.select_related("lecturer")

    def get_object(self, queryset=None):
        course = super().get_object(queryset)
        if not course.can_access(self.request.user):
            raise PermissionDenied
        return course

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        user = self.request.user
        course = self.object

        context["can_manage"] = course.can_manage(user)
        context["student_count"] = course.enrollments.filter(
            status=Enrollment.Status.ACTIVE
        ).count()
        context["materials"] = course.materials.order_by("meeting_no", "title")
        assignments = course.assignments.order_by("due_at")
        context["assignments"] = assignments
        context["announcements"] = course.announcements.order_by("-published_at")

        if user.is_mahasiswa:
            submissions = {
                submission.assignment_id: submission
                for submission in user.submissions.filter(assignment__course=course)
            }
            context["my_submissions"] = submissions
            context["assignment_rows"] = [
                {"assignment": assignment, "submission": submissions.get(assignment.id)}
                for assignment in assignments
            ]
        else:
            context["assignment_rows"] = [
                {"assignment": assignment, "submission": None} for assignment in assignments
            ]
            context["participants"] = (
                course.enrollments.filter(status=Enrollment.Status.ACTIVE)
                .select_related("student")
                .order_by("student__full_name")
            )
        return context


@require_POST
@role_required("mahasiswa")
def enroll(request, pk):
    course = get_object_or_404(Course, pk=pk)
    if course.is_archived:
        messages.error(request, "Mata kuliah telah diarsipkan dan tidak dapat didaftar.")
        return redirect("courses:list")

    enrollment, created = Enrollment.objects.get_or_create(
        course=course,
        student=request.user,
        defaults={"status": Enrollment.Status.ACTIVE},
    )
    if not created and enrollment.status == Enrollment.Status.DROPPED:
        enrollment.status = Enrollment.Status.ACTIVE
        enrollment.save(update_fields=["status"])
        created = True

    if created:
        messages.success(request, f"Anda terdaftar pada {course.code} — {course.name}.")
    else:
        messages.info(request, "Anda sudah terdaftar pada mata kuliah ini.")
    return redirect("courses:detail", pk=course.pk)
