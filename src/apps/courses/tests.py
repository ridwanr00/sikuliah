"""Pengujian otomatis akses mata kuliah dan enrollment (FR-01, FR-04)."""

from django.test import TestCase

from apps.accounts.models import Role, User

from .models import Course, Enrollment


class CourseAccessTests(TestCase):
    def setUp(self):
        self.lecturer = User.objects.create_user(
            email="dosen@test.id",
            password="rahasia123",
            full_name="Dosen Uji",
            identity_number="D-1",
            role=Role.DOSEN,
        )
        self.other = User.objects.create_user(
            email="dosen2@test.id",
            password="rahasia123",
            full_name="Dosen Lain",
            identity_number="D-2",
            role=Role.DOSEN,
        )
        self.student = User.objects.create_user(
            email="mhs@test.id",
            password="rahasia123",
            full_name="Mahasiswa Uji",
            identity_number="M-1",
            role=Role.MAHASISWA,
        )
        self.course = Course.objects.create(
            code="IF-998",
            name="Mata Kuliah Uji",
            credits=3,
            lecturer=self.lecturer,
        )

    def test_mahasiswa_belum_terdaftar_mendapat_403(self):
        self.client.force_login(self.student)
        response = self.client.get(f"/mata-kuliah/{self.course.pk}/")
        self.assertEqual(response.status_code, 403)

    def test_mahasiswa_terdaftar_dapat_membuka(self):
        Enrollment.objects.create(course=self.course, student=self.student)
        self.client.force_login(self.student)
        response = self.client.get(f"/mata-kuliah/{self.course.pk}/")
        self.assertEqual(response.status_code, 200)

    def test_enrollment_ganda_tidak_terjadi(self):
        self.client.force_login(self.student)
        url = f"/mata-kuliah/{self.course.pk}/daftar/"
        self.client.post(url)
        self.client.post(url)
        self.assertEqual(
            Enrollment.objects.filter(course=self.course, student=self.student).count(), 1
        )

    def test_dosen_bukan_pengampu_mendapat_403(self):
        self.client.force_login(self.other)
        response = self.client.get(f"/mata-kuliah/{self.course.pk}/")
        self.assertEqual(response.status_code, 403)

    def test_pengguna_belum_login_diarahkan_ke_login(self):
        response = self.client.get(f"/mata-kuliah/{self.course.pk}/")
        self.assertEqual(response.status_code, 302)
        self.assertIn("/masuk/", response["Location"])

    def test_mahasiswa_tidak_dapat_membuat_tugas(self):
        Enrollment.objects.create(course=self.course, student=self.student)
        self.client.force_login(self.student)
        response = self.client.get(f"/tugas/baru/{self.course.pk}/")
        self.assertEqual(response.status_code, 403)
