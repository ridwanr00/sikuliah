"""View autentikasi dan halaman publik."""

from django.contrib.auth.views import LoginView as DjangoLoginView
from django.contrib.auth.views import LogoutView as DjangoLogoutView
from django.shortcuts import render


class LoginView(DjangoLoginView):
    template_name = "registration/login.html"
    redirect_authenticated_user = True

    def form_invalid(self, form):
        # Pesan generik: jangan mengungkap bagian kredensial mana yang salah (AC-01.2).
        form.add_error(None, "Surel atau kata sandi tidak sesuai.")
        return super().form_invalid(form)


class LogoutView(DjangoLogoutView):
    next_page = "/"


def home(request):
    return render(request, "home.html")


def error_403(request, exception=None):
    return render(request, "errors/403.html", status=403)


def error_404(request, exception=None):
    return render(request, "errors/404.html", status=404)


def error_500(request):
    return render(request, "errors/500.html", status=500)
