"""View tugas: buat, lihat, kumpulkan, nilai (FR-06, FR-07, FR-08)."""

from pathlib import Path

from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.exceptions import PermissionDenied
from django.db.models import Avg, Count, Q
from django.http import FileResponse, Http404
from django.shortcuts import get_object_or_404, redirect, render
from django.urls import reverse_lazy
from django.utils import timezone
from django.views.decorators.http import require_POST
from django.views.generic import CreateView

from apps.accounts.mixins import RoleRequiredMixin, role_required
from apps.courses.models import Course, Enrollment

from .forms import AssignmentForm, GradeForm, SubmissionForm
from .models import Assignment, Submission


class AssignmentCreateView(RoleRequiredMixin, CreateView):
    allowed_roles = ("dosen", "admin")
    model = Assignment
    form_class = AssignmentForm
    template_name = "assignments/assignment_form.html"

    def get_course(self) -> Course:
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        if not course.can_manage(self.request.user):
            raise PermissionDenied
        return course

    def form_valid(self, form):
        form.instance.course = self.get_course()
        messages.success(self.request, "Tugas berhasil dibuat.")
        return super().form_valid(form)

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.get_course()
        return context

    def get_success_url(self):
        return reverse_lazy("courses:detail", kwargs={"pk": self.kwargs["course_id"]})


@login_required
def assignment_detail(request, pk):
    assignment = get_object_or_404(
        Assignment.objects.select_related("course", "course__lecturer"), pk=pk
    )
    if not assignment.course.can_access(request.user):
        raise PermissionDenied

    submission = None
    if request.user.is_mahasiswa:
        submission = Submission.objects.filter(assignment=assignment, student=request.user).first()

    context = {
        "assignment": assignment,
        "course": assignment.course,
        "submission": submission,
        "form": SubmissionForm(),
        "can_submit": (
            request.user.is_mahasiswa
            and not assignment.is_past_due
            and (submission is None or not submission.is_graded)
        ),
    }
    return render(request, "assignments/assignment_detail.html", context)


@require_POST
@role_required("mahasiswa")
def submit(request, pk):
    assignment = get_object_or_404(Assignment.objects.select_related("course"), pk=pk)
    if not assignment.course.is_participant(request.user):
        raise PermissionDenied

    # AC-07.2: tenggat diperiksa di server, bukan mengandalkan status tombol di template.
    if assignment.is_past_due:
        messages.error(request, "Tenggat telah berakhir. Pengumpulan ditolak.")
        return redirect("assignments:detail", pk=assignment.pk)

    existing = Submission.objects.filter(assignment=assignment, student=request.user).first()
    if existing and existing.is_graded:
        messages.error(request, "Tugas sudah dinilai, berkas tidak dapat diganti.")
        return redirect("assignments:detail", pk=assignment.pk)

    form = SubmissionForm(request.POST, request.FILES)
    if not form.is_valid():
        for error in form.errors.get("file", []):
            messages.error(request, error)
        return redirect("assignments:detail", pk=assignment.pk)

    uploaded = form.cleaned_data["file"]
    if existing:
        existing.file = uploaded
        existing.original_filename = Path(uploaded.name).name
        existing.submitted_at = timezone.now()
        existing.save()
        messages.success(request, "Berkas pengganti berhasil diunggah.")
    else:
        Submission.objects.create(
            assignment=assignment,
            student=request.user,
            file=uploaded,
            original_filename=Path(uploaded.name).name,
            submitted_at=timezone.now(),
        )
        messages.success(request, "Tugas berhasil dikumpulkan.")
    return redirect("assignments:detail", pk=assignment.pk)


@login_required
def submission_list(request, pk):
    assignment = get_object_or_404(Assignment.objects.select_related("course"), pk=pk)
    if not assignment.course.can_manage(request.user):
        raise PermissionDenied

    participants = Enrollment.objects.filter(
        course=assignment.course, status=Enrollment.Status.ACTIVE
    ).select_related("student")
    submissions = {
        submission.student_id: submission
        for submission in assignment.submissions.select_related("student")
    }
    rows = [
        {"student": enrollment.student, "submission": submissions.get(enrollment.student_id)}
        for enrollment in participants
    ]
    rows.sort(key=lambda row: row["student"].full_name)

    stats = assignment.submissions.aggregate(
        total=Count("id"),
        graded=Count("id", filter=Q(score__isnull=False)),
        average=Avg("score"),
    )
    context = {
        "assignment": assignment,
        "course": assignment.course,
        "rows": rows,
        "total_students": len(rows),
        "submitted": stats["total"],
        "graded": stats["graded"],
        "average": stats["average"],
        "query": request.GET.get("q", "").strip(),
    }
    if context["query"]:
        needle = context["query"].lower()
        context["rows"] = [
            row
            for row in rows
            if needle in row["student"].full_name.lower()
            or needle in row["student"].identity_number.lower()
        ]
    return render(request, "assignments/submission_list.html", context)


@login_required
def grade(request, pk):
    submission = get_object_or_404(
        Submission.objects.select_related("assignment", "assignment__course", "student"),
        pk=pk,
    )
    if not submission.assignment.course.can_manage(request.user):
        raise PermissionDenied

    if request.method == "POST":
        form = GradeForm(request.POST, instance=submission)
        if form.is_valid():
            graded = form.save(commit=False)
            graded.graded_at = timezone.now()
            graded.save()
            messages.success(
                request,
                f"Nilai {graded.score} untuk {graded.student.full_name} berhasil disimpan.",
            )
            return redirect("assignments:submissions", pk=submission.assignment_id)
    else:
        form = GradeForm(instance=submission)

    return render(
        request,
        "assignments/grade_form.html",
        {"form": form, "submission": submission, "assignment": submission.assignment},
    )


@login_required
def download_submission(request, pk):
    submission = get_object_or_404(
        Submission.objects.select_related("assignment", "assignment__course"), pk=pk
    )
    is_owner = submission.student_id == request.user.id
    if not (is_owner or submission.assignment.course.can_manage(request.user)):
        raise PermissionDenied

    # Berkas bisa hilang (disk sementara hosting) meski record masih ada.
    # Itu bukan masalah izin: kembalikan 404 agar pesannya tidak menyesatkan.
    if not submission.file or not submission.file.storage.exists(submission.file.name):
        raise Http404(
            "Berkas pengumpulan tidak ditemukan pada penyimpanan. "
            "Minta mahasiswa mengunggah ulang atau aktifkan object storage."
        )
    handle = submission.file.open("rb")
    return FileResponse(handle, as_attachment=True, filename=submission.original_filename)
