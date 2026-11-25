"""Perintah seed data demo: python manage.py seed_demo

Membuat data yang cukup untuk demonstrasi dan pengujian TC-01…TC-08:
1 admin, 4 dosen, 30 mahasiswa, 6 mata kuliah, materi (berkas PDF asli),
12 tugas (sebagian lewat tenggat), dan ± 60% pengumpulan dengan nilai.
"""

import random
import secrets
from datetime import timedelta

from decouple import config
from django.core.files.base import ContentFile
from django.core.management.base import BaseCommand
from django.utils import timezone

from apps.announcements.models import Announcement
from apps.assignments.models import Assignment, Submission
from apps.courses.models import Course, Enrollment
from apps.materials.models import Material

from ...models import Role, User


def demo_passwords() -> tuple[str, str, str, str | None]:
    """Ambil kata sandi demo dari environment.

    Tidak ada kata sandi yang ditulis di kode/repositori. Bila environment tidak
    diisi, satu kata sandi acak dibuat dan dicetak sekali agar tetap dapat dipakai.
    """
    base = config("DEMO_PASSWORD", default="")
    generated = None if base else secrets.token_urlsafe(9)
    fallback = base or generated
    return (
        config("DEMO_ADMIN_PASSWORD", default=fallback),
        config("DEMO_DOSEN_PASSWORD", default=fallback),
        config("DEMO_MAHASISWA_PASSWORD", default=fallback),
        generated,
    )


def minimal_pdf(title: str, body: str) -> bytes:
    """Membuat PDF satu halaman yang valid tanpa dependensi eksternal."""
    content = f"BT /F1 14 Tf 50 780 Td 20 TL ({title}) Tj T* /F1 10 Tf ({body}) Tj T* ET"
    objects = [
        "<< /Type /Catalog /Pages 2 0 R >>",
        "<< /Type /Pages /Kids [3 0 R] /Count 1 >>",
        "<< /Type /Page /Parent 2 0 R /MediaBox [0 0 595 842] "
        "/Resources << /Font << /F1 4 0 R >> >> /Contents 5 0 R >>",
        "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>",
        f"<< /Length {len(content)} >>\nstream\n{content}\nendstream",
    ]
    out = "%PDF-1.4\n"
    offsets = []
    for index, obj in enumerate(objects, start=1):
        offsets.append(len(out))
        out += f"{index} 0 obj\n{obj}\nendobj\n"
    xref_offset = len(out)
    out += f"xref\n0 {len(objects) + 1}\n0000000000 65535 f \n"
    out += "".join(f"{offset:010d} 00000 n \n" for offset in offsets)
    out += f"trailer\n<< /Size {len(objects) + 1} /Root 1 0 R >>\nstartxref\n{xref_offset}\n%%EOF\n"
    return out.encode("latin-1", errors="replace")


class Command(BaseCommand):
    help = "Mengisi basis data dengan data demo SIKULIAH (idempoten)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--no-refresh-files",
            action="store_true",
            help="Jangan buat ulang berkas demo yang hilang dari penyimpanan.",
        )

    def refresh_missing_files(self) -> tuple[int, int]:
        """Buat ulang berkas demo yang recordnya ada tetapi filenya hilang.

        Terjadi ketika hosting memakai disk sementara: basis data tetap, berkas
        terhapus saat restart. Hanya menyentuh berkas contoh (PDF sintetis).
        """
        restored = 0
        failed = 0

        for material in Material.objects.select_related("course"):
            if not material.file:
                continue
            try:
                if material.file.storage.exists(material.file.name):
                    continue
                payload = minimal_pdf(
                    f"{material.course.code} - Pertemuan {material.meeting_no}",
                    f"Materi: {material.title} (dipulihkan dari data demo).",
                )
                material.file.save(
                    f"{material.course.code.lower()}-pertemuan-{material.meeting_no}.pdf",
                    ContentFile(payload),
                    save=True,
                )
                restored += 1
            except Exception:  # noqa: BLE001 - jangan hentikan seed karena satu berkas
                failed += 1

        for submission in Submission.objects.select_related("student", "assignment"):
            if not submission.file:
                continue
            try:
                if submission.file.storage.exists(submission.file.name):
                    continue
                payload = minimal_pdf(
                    f"Jawaban {submission.assignment.title}",
                    f"Mahasiswa: {submission.student.full_name} (dipulihkan dari data demo).",
                )
                submission.file.save(
                    f"jawaban-{submission.student.identity_number}.pdf",
                    ContentFile(payload),
                    save=True,
                )
                restored += 1
            except Exception:  # noqa: BLE001
                failed += 1

        return restored, failed

    def handle(self, *args, **options):
        random.seed(42)
        now = timezone.now()
        admin_pw, dosen_pw, mahasiswa_pw, generated_pw = demo_passwords()
        force_password = config("FORCE_DEMO_PASSWORD", default=False, cast=bool)

        def apply_password(user, password, is_new):
            # Hanya menimpa kata sandi bila akun baru atau FORCE_DEMO_PASSWORD aktif,
            # supaya perubahan manual tidak hilang tanpa sengaja.
            if is_new or force_password:
                user.set_password(password)
                user.save(update_fields=["password"])

        self.generated_pw = generated_pw

        admin, created = User.objects.get_or_create(
            email="admin@kampus.test",
            defaults={
                "full_name": "Admin Akademik",
                "identity_number": "ADMIN-001",
                "role": Role.ADMIN,
                "is_staff": True,
                "is_superuser": True,
            },
        )
        apply_password(admin, admin_pw, created)
        if created:
            self.stdout.write("  + admin@kampus.test")

        lecturers = []
        lecturer_names = [
            ("Anas Nasrulloh", "D001"),
            ("Siti Rahmawati", "D002"),
            ("Budi Hartono", "D003"),
            ("Dewi Kartika", "D004"),
        ]
        for index, (name, nidn) in enumerate(lecturer_names, start=1):
            lecturer, created = User.objects.get_or_create(
                email=f"dosen{index}@kampus.test",
                defaults={
                    "full_name": name,
                    "identity_number": nidn,
                    "role": Role.DOSEN,
                },
            )
            apply_password(lecturer, dosen_pw, created)
            lecturers.append(lecturer)

        students = []
        for index in range(1, 31):
            student, created = User.objects.get_or_create(
                email=f"mhs{index:02d}@kampus.test",
                defaults={
                    "full_name": f"Mahasiswa {index:02d}",
                    "identity_number": f"2026{index:04d}",
                    "role": Role.MAHASISWA,
                },
            )
            apply_password(student, mahasiswa_pw, created)
            students.append(student)

        courses_data = [
            ("IF-301", "Rekayasa Perangkat Lunak", 3, 0),
            ("IF-302", "Basis Data Lanjut", 3, 1),
            ("IF-303", "Pemrograman Web", 3, 1),
            ("IF-304", "Jaringan Komputer", 2, 2),
            ("IF-305", "Analisis dan Desain Sistem", 3, 0),
            ("IF-306", "Kecerdasan Buatan", 3, 3),
        ]
        courses = []
        for code, name, credits, lecturer_index in courses_data:
            course, _ = Course.objects.get_or_create(
                code=code,
                defaults={
                    "name": name,
                    "credits": credits,
                    "semester": Course.Semester.GANJIL,
                    "academic_year": "2026/2027",
                    "description": f"Mata kuliah {name} semester ganjil 2026/2027.",
                    "lecturer": lecturers[lecturer_index],
                },
            )
            courses.append(course)

        # Enrollment: setiap mahasiswa mengambil 3 mata kuliah berbeda.
        # mhs01 terdaftar di IF-301; mhs09 sengaja TIDAK terdaftar di IF-301 (TC-07).
        for index, student in enumerate(students):
            picks = {0, (index % 5) + 1, (index % 4) + 2}
            if student.email == "mhs09@kampus.test":
                picks.discard(0)
            for pick in sorted(picks):
                Enrollment.objects.get_or_create(
                    course=courses[pick],
                    student=student,
                    defaults={"status": Enrollment.Status.ACTIVE},
                )

        # Materi: 4 per mata kuliah, berkas PDF nyata di media/materials/.
        material_topics = [
            "Pengantar dan Kontrak Kuliah",
            "Kebutuhan Fungsional dan Nonfungsional",
            "Pemodelan Use Case",
            "Studi Kasus dan Latihan",
        ]
        for course in courses:
            for meeting, topic in enumerate(material_topics, start=1):
                if course.materials.filter(meeting_no=meeting).exists():
                    continue
                material = Material(
                    course=course,
                    title=f"{topic}",
                    meeting_no=meeting,
                    description=f"Materi pertemuan {meeting} untuk {course.name}.",
                    is_required=meeting <= 2,
                )
                payload = minimal_pdf(
                    f"{course.code} - Pertemuan {meeting}",
                    f"Materi: {topic}. Dokumen demo SIKULIAH.",
                )
                material.file.save(
                    f"{course.code.lower()}-pertemuan-{meeting}.pdf",
                    ContentFile(payload),
                    save=False,
                )
                material.save()

        # Tugas: 2 per mata kuliah; satu lewat tenggat, satu masih aktif.
        for course in courses:
            if course.assignments.count() >= 2:
                continue
            Assignment.objects.create(
                course=course,
                title="Tugas 1 — Analisis Kebutuhan",
                description=(
                    "Susun analisis kebutuhan untuk studi kasus yang diberikan. "
                    "Kumpulkan dalam format PDF maksimal 5 MB."
                ),
                due_at=now - timedelta(days=6),
                max_score=100,
            )
            Assignment.objects.create(
                course=course,
                title="Tugas 2 — Perancangan Sistem",
                description=(
                    "Buat rancangan use case dan ERD, lalu jelaskan alur interaksinya. "
                    "Kumpulkan dalam format PDF."
                ),
                due_at=now + timedelta(days=4),
                max_score=100,
            )

        # Pengumpulan: tingkat partisipasi menurun pada tugas ke-2 (bahan temuan video).
        rates = [0.88, 0.62]
        for course in courses:
            enrolled = list(
                course.enrollments.filter(status=Enrollment.Status.ACTIVE).select_related("student")
            )
            for order, assignment in enumerate(course.assignments.order_by("due_at")):
                if assignment.submissions.exists():
                    continue  # sudah pernah di-seed; jangan menambah data baru
                rate = rates[min(order, len(rates) - 1)]
                for enrollment in enrolled:
                    if random.random() > rate:
                        continue
                    if Submission.objects.filter(
                        assignment=assignment, student=enrollment.student
                    ).exists():
                        continue
                    score = None
                    graded_at = None
                    if random.random() < 0.75:
                        score = random.randint(60, 95)
                        graded_at = now - timedelta(days=random.randint(1, 5))
                    submission = Submission(
                        assignment=assignment,
                        student=enrollment.student,
                        original_filename="jawaban.pdf",
                        submitted_at=assignment.due_at - timedelta(hours=random.randint(1, 40)),
                        score=score,
                        graded_at=graded_at,
                        feedback=(
                            "Struktur sudah baik. Tambahkan matriks keterlacakan "
                            "dan perjelas asumsi sistem."
                            if score is not None
                            else ""
                        ),
                    )
                    payload = minimal_pdf(
                        f"Jawaban {assignment.title}",
                        f"Mahasiswa: {enrollment.student.full_name}",
                    )
                    submission.file.save(
                        f"jawaban-{enrollment.student.identity_number}.pdf",
                        ContentFile(payload),
                        save=False,
                    )
                    submission.save()

        # Pengumuman
        for course in courses[:3]:
            Announcement.objects.get_or_create(
                course=course,
                title="Perubahan jadwal pertemuan",
                defaults={
                    "body": "Pertemuan pekan ini dimajukan satu hari. "
                    "Materi tetap dapat diunduh dari halaman mata kuliah."
                },
            )

        if options.get("no_refresh_files"):
            restored, failed = 0, 0
        else:
            restored, failed = self.refresh_missing_files()

        self.stdout.write(self.style.SUCCESS("\nData demo siap."))
        if restored or failed:
            self.stdout.write(
                f"  berkas demo dipulihkan: {restored}"
                + (f", gagal: {failed}" if failed else "")
            )
        self.stdout.write("  admin@kampus.test, dosen1@kampus.test, mhs01@kampus.test")
        if generated_pw:
            self.stdout.write(
                self.style.WARNING(
                    f"  Kata sandi demo dibuat otomatis: {generated_pw}\n"
                    "  Catat sekarang; set DEMO_PASSWORD agar nilainya tetap."
                )
            )
        else:
            self.stdout.write("  Kata sandi demo diambil dari environment (tidak ditampilkan).")
        self.stdout.write(
            f"  {User.objects.count()} pengguna, {Course.objects.count()} mata kuliah, "
            f"{Material.objects.count()} materi, {Assignment.objects.count()} tugas, "
            f"{Submission.objects.count()} pengumpulan."
        )
