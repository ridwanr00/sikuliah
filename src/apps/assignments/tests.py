"""Pengujian otomatis alur tugas (FR-07, FR-08)."""

from datetime import timedelta

from django.core.files.uploadedfile import SimpleUploadedFile
from django.test import TestCase
from django.utils import timezone

from apps.accounts.models import Role, User
from apps.courses.models import Course, Enrollment

from .models import Assignment, Submission


def make_pdf(name="jawaban.pdf"):
    return SimpleUploadedFile(name, b"%PDF-1.4 contoh", content_type="application/pdf")


class SubmissionFlowTests(TestCase):
    def setUp(self):
        self.lecturer = User.objects.create_user(
            email="dosen@test.id",
            password="rahasia123",
            full_name="Dosen Uji",
            identity_number="D-1",
            role=Role.DOSEN,
        )
        self.other_lecturer = User.objects.create_user(
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
        self.outsider = User.objects.create_user(
            email="luar@test.id",
            password="rahasia123",
            full_name="Mahasiswa Luar",
            identity_number="M-2",
            role=Role.MAHASISWA,
        )
        self.course = Course.objects.create(
            code="IF-999",
            name="Mata Kuliah Uji",
            credits=3,
            lecturer=self.lecturer,
        )
        Enrollment.objects.create(course=self.course, student=self.student)
        self.assignment = Assignment.objects.create(
            course=self.course,
            title="Tugas Uji",
            description="Kerjakan.",
            due_at=timezone.now() + timedelta(days=2),
            max_score=100,
        )

    def test_mahasiswa_dapat_mengumpulkan_sebelum_tenggat(self):
        self.client.force_login(self.student)
        response = self.client.post(f"/tugas/{self.assignment.pk}/kumpulkan/", {"file": make_pdf()})
        self.assertEqual(response.status_code, 302)
        self.assertTrue(
            Submission.objects.filter(assignment=self.assignment, student=self.student).exists()
        )

    def test_pengumpulan_setelah_tenggat_ditolak(self):
        self.assignment.due_at = timezone.now() - timedelta(hours=1)
        self.assignment.save()
        self.client.force_login(self.student)
        self.client.post(f"/tugas/{self.assignment.pk}/kumpulkan/", {"file": make_pdf()})
        self.assertFalse(
            Submission.objects.filter(assignment=self.assignment, student=self.student).exists()
        )

    def test_ekstensi_terlarang_ditolak(self):
        self.client.force_login(self.student)
        bad = SimpleUploadedFile("virus.exe", b"MZ", content_type="application/octet-stream")
        self.client.post(f"/tugas/{self.assignment.pk}/kumpulkan/", {"file": bad})
        self.assertFalse(
            Submission.objects.filter(assignment=self.assignment, student=self.student).exists()
        )

    def test_unggah_ulang_tidak_menduplikasi(self):
        self.client.force_login(self.student)
        url = f"/tugas/{self.assignment.pk}/kumpulkan/"
        self.client.post(url, {"file": make_pdf("satu.pdf")})
        self.client.post(url, {"file": make_pdf("dua.pdf")})
        self.assertEqual(
            Submission.objects.filter(assignment=self.assignment, student=self.student).count(),
            1,
        )

    def test_mahasiswa_luar_tidak_dapat_mengumpulkan(self):
        self.client.force_login(self.outsider)
        response = self.client.post(f"/tugas/{self.assignment.pk}/kumpulkan/", {"file": make_pdf()})
        self.assertEqual(response.status_code, 403)

    def test_nilai_di_luar_rentang_ditolak(self):
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            file=make_pdf(),
            original_filename="jawaban.pdf",
        )
        self.client.force_login(self.lecturer)
        url = f"/tugas/pengumpulan/{submission.pk}/nilai/"
        response = self.client.post(url, {"score": 101, "feedback": ""})
        self.assertEqual(response.status_code, 200)
        submission.refresh_from_db()
        self.assertIsNone(submission.score)

    def test_dosen_lain_tidak_dapat_menilai(self):
        submission = Submission.objects.create(
            assignment=self.assignment,
            student=self.student,
            file=make_pdf(),
            original_filename="jawaban.pdf",
        )
        self.client.force_login(self.other_lecturer)
        response = self.client.get(f"/tugas/pengumpulan/{submission.pk}/nilai/")
        self.assertEqual(response.status_code, 403)
