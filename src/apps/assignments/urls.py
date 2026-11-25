from django.urls import path

from . import views

app_name = "assignments"

urlpatterns = [
    path("baru/<int:course_id>/", views.AssignmentCreateView.as_view(), name="create"),
    path("<int:pk>/", views.assignment_detail, name="detail"),
    path("<int:pk>/kumpulkan/", views.submit, name="submit"),
    path("<int:pk>/pengumpulan/", views.submission_list, name="submissions"),
    path("pengumpulan/<int:pk>/nilai/", views.grade, name="grade"),
    path("pengumpulan/<int:pk>/unduh/", views.download_submission, name="download"),
]
