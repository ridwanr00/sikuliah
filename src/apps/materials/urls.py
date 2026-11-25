from django.urls import path

from . import views

app_name = "materials"

urlpatterns = [
    path("tambah/<int:course_id>/", views.MaterialCreateView.as_view(), name="create"),
    path("<int:course_id>/ubah/<int:pk>/", views.MaterialUpdateView.as_view(), name="update"),
    path("<int:course_id>/hapus/<int:pk>/", views.MaterialDeleteView.as_view(), name="delete"),
    path("<int:pk>/unduh/", views.download, name="download"),
]
