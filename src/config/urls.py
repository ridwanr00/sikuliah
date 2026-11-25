"""URL utama proyek SIKULIAH."""

from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path, re_path

from apps.accounts.views import LoginView, LogoutView, home

urlpatterns = [
    path("", home, name="home"),
    path("masuk/", LoginView.as_view(), name="login"),
    path("keluar/", LogoutView.as_view(), name="logout"),
    path("dasbor/", include("apps.dashboard.urls")),
    path("mata-kuliah/", include("apps.courses.urls")),
    path("materi/", include("apps.materials.urls")),
    path("tugas/", include("apps.assignments.urls")),
    path("pengumuman/", include("apps.announcements.urls")),
    path("admin/", admin.site.urls),
]

# Berkas media hanya disajikan Django bila memakai penyimpanan lokal.
# Jika USE_S3_STORAGE aktif, berkas berada di bucket dan diakses lewat URL bertanda tangan.
if not settings.USE_S3_STORAGE:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

    if not settings.DEBUG:
        from django.views.static import serve

        urlpatterns += [
            re_path(r"^media/(?P<path>.*)$", serve, {"document_root": settings.MEDIA_ROOT})
        ]

handler403 = "apps.accounts.views.error_403"
handler404 = "apps.accounts.views.error_404"
handler500 = "apps.accounts.views.error_500"

admin.site.site_header = "SIKULIAH — Panel Admin"
admin.site.site_title = "SIKULIAH"
admin.site.index_title = "Pengelolaan data akademik"
