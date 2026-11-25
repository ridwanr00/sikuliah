from django.urls import path

from . import views

app_name = "announcements"

urlpatterns = [
    path("tambah/<int:course_id>/", views.AnnouncementCreateView.as_view(), name="create"),
    path("<int:course_id>/hapus/<int:pk>/", views.AnnouncementDeleteView.as_view(), name="delete"),
]
