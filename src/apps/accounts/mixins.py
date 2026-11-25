"""Kontrol akses berbasis peran (FR-01)."""

from functools import wraps

from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import redirect_to_login
from django.core.exceptions import PermissionDenied


class RoleRequiredMixin(LoginRequiredMixin):
    """Batasi view kelas berdasarkan peran pengguna.

    Otorisasi diperiksa di server pada setiap permintaan (NFR-02), bukan hanya dengan
    menyembunyikan menu di template.
    """

    allowed_roles: tuple[str, ...] = ()

    def dispatch(self, request, *args, **kwargs):
        if request.user.is_authenticated and self.allowed_roles:
            if request.user.role not in self.allowed_roles:
                raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)


def role_required(*roles):
    """Versi dekorator untuk view berbasis fungsi."""

    def decorator(view_func):
        @wraps(view_func)
        def _wrapped(request, *args, **kwargs):
            if not request.user.is_authenticated:
                return redirect_to_login(request.get_full_path())
            if request.user.role not in roles:
                raise PermissionDenied
            return view_func(request, *args, **kwargs)

        return _wrapped

    return decorator
