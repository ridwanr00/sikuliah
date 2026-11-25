"""View pengumuman (FR-09)."""

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView

from apps.accounts.mixins import RoleRequiredMixin
from apps.courses.models import Course

from .forms import AnnouncementForm
from .models import Announcement


class AnnouncementMixin(RoleRequiredMixin):
    allowed_roles = ("dosen", "admin")
    model = Announcement
    form_class = AnnouncementForm
    template_name = "announcements/announcement_form.html"

    def get_course(self) -> Course:
        course = get_object_or_404(Course, pk=self.kwargs["course_id"])
        if not course.can_manage(self.request.user):
            raise PermissionDenied
        return course

    def get_success_url(self):
        return reverse_lazy("courses:detail", kwargs={"pk": self.kwargs["course_id"]})

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context["course"] = self.get_course()
        return context


class AnnouncementCreateView(AnnouncementMixin, CreateView):
    def form_valid(self, form):
        form.instance.course = self.get_course()
        messages.success(self.request, "Pengumuman diterbitkan.")
        return super().form_valid(form)


class AnnouncementDeleteView(AnnouncementMixin, DeleteView):
    template_name = "announcements/announcement_confirm_delete.html"

    def get_queryset(self):
        return Announcement.objects.filter(course_id=self.kwargs["course_id"])

    def form_valid(self, form):
        messages.success(self.request, "Pengumuman dihapus.")
        return super().form_valid(form)
