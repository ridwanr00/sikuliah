"""View materi: unggah, ubah, hapus, unduh (FR-05)."""

from pathlib import Path

from django.contrib import messages
from django.core.exceptions import PermissionDenied
from django.http import FileResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.urls import reverse_lazy
from django.views.generic import CreateView, DeleteView, UpdateView

from apps.accounts.mixins import RoleRequiredMixin
from apps.courses.models import Course

from .forms import MaterialForm
from .models import Material


class MaterialFormMixin(RoleRequiredMixin):
    allowed_roles = ("dosen", "admin")
    model = Material
    form_class = MaterialForm
    template_name = "materials/material_form.html"

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


class MaterialCreateView(MaterialFormMixin, CreateView):
    def form_valid(self, form):
        form.instance.course = self.get_course()
        messages.success(self.request, "Materi berhasil diunggah.")
        return super().form_valid(form)


class MaterialUpdateView(MaterialFormMixin, UpdateView):
    def get_queryset(self):
        return Material.objects.filter(course_id=self.kwargs["course_id"])

    def form_valid(self, form):
        messages.success(self.request, "Materi berhasil diperbarui.")
        return super().form_valid(form)


class MaterialDeleteView(MaterialFormMixin, DeleteView):
    template_name = "materials/material_confirm_delete.html"

    def get_queryset(self):
        return Material.objects.filter(course_id=self.kwargs["course_id"])

    def form_valid(self, form):
        messages.success(self.request, "Materi dihapus.")
        return super().form_valid(form)


def download(request, pk):
    material = get_object_or_404(Material.objects.select_related("course"), pk=pk)
    if not material.course.can_access(request.user):
        raise PermissionDenied

    if material.external_url:
        return HttpResponseRedirect(material.external_url)

    if not material.file:
        raise Http404("Berkas materi tidak tersedia.")

    try:
        handle = material.file.open("rb")
    except FileNotFoundError as exc:
        raise Http404("Berkas materi tidak ditemukan di penyimpanan.") from exc

    filename = Path(material.file.name).name
    return FileResponse(handle, as_attachment=True, filename=filename)
