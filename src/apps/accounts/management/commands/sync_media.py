"""Sinkronkan berkas media lokal ke object storage yang aktif.

Pemakaian:
    python manage.py sync_media --check     # uji kredensial bucket
    python manage.py sync_media --dry-run   # lihat apa yang akan diunggah
    python manage.py sync_media             # unggah berkas yang belum ada di bucket

Berguna saat baru mengaktifkan USE_S3_STORAGE: berkas yang sudah ada di media/
tidak otomatis pindah, hanya unggahan baru yang masuk ke bucket.
"""

from pathlib import Path

from django.conf import settings
from django.core.files import File
from django.core.files.base import ContentFile
from django.core.files.storage import default_storage
from django.core.management.base import BaseCommand, CommandError

from apps.assignments.models import Assignment, Submission
from apps.materials.models import Material


class Command(BaseCommand):
    help = "Unggah berkas media lokal yang belum ada di object storage aktif."

    def add_arguments(self, parser):
        parser.add_argument(
            "--dry-run", action="store_true", help="Tampilkan rencana tanpa mengunggah."
        )
        parser.add_argument(
            "--check",
            action="store_true",
            help="Uji kredensial: tulis lalu hapus satu objek kecil di bucket.",
        )

    def handle(self, *args, **options):
        if not settings.USE_S3_STORAGE:
            raise CommandError(
                "USE_S3_STORAGE belum aktif. Isi USE_S3_STORAGE=True beserta AWS_* "
                "di environment sebelum menjalankan perintah ini."
            )

        storage = default_storage

        if options["check"]:
            self.check_credentials(storage)
            return

        targets = []
        for material in Material.objects.exclude(file="").select_related("course"):
            targets.append((material, "file", f"materi #{material.pk}"))
        for submission in Submission.objects.exclude(file="").select_related("student"):
            targets.append((submission, "file", f"pengumpulan #{submission.pk}"))
        for assignment in Assignment.objects.exclude(attachment="").select_related("course"):
            targets.append((assignment, "attachment", f"lampiran tugas #{assignment.pk}"))

        uploaded = skipped = missing = 0
        missing_names: list[str] = []

        for obj, field_name, label in targets:
            field = getattr(obj, field_name)
            name = field.name
            if not name:
                continue

            try:
                if storage.exists(name):
                    skipped += 1
                    continue
            except Exception as exc:  # noqa: BLE001 - tampilkan error storage apa adanya
                raise CommandError(f"Gagal memeriksa bucket: {exc}") from exc

            local_path = Path(settings.MEDIA_ROOT) / name
            if not local_path.exists():
                missing += 1
                if len(missing_names) < 10:
                    missing_names.append(name)
                continue

            if options["dry_run"]:
                self.stdout.write(f"[dry-run] {label}: {name}")
                uploaded += 1
                continue

            with local_path.open("rb") as handle:
                saved_name = storage.save(name, File(handle))
            setattr(obj, field_name, saved_name)
            obj.save(update_fields=[field_name])
            uploaded += 1
            if uploaded % 20 == 0:
                self.stdout.write(f"  ... {uploaded} berkas diunggah")

        if options["dry_run"]:
            self.stdout.write(
                f"Rencana: {uploaded} akan diunggah, {skipped} sudah ada, "
                f"{missing} tidak ditemukan di media lokal."
            )
            return

        self.stdout.write(
            self.style.SUCCESS(
                f"Selesai: {uploaded} diunggah, {skipped} dilewati (sudah ada), "
                f"{missing} tidak ditemukan di media lokal."
            )
        )
        if missing_names:
            self.stdout.write(
                "Berkas yang tidak ada di media lokal (perlu unggah ulang lewat aplikasi):"
            )
            for name in missing_names:
                self.stdout.write(f"  - {name}")
            if missing > len(missing_names):
                self.stdout.write(f"  ... dan {missing - len(missing_names)} lainnya")

    def check_credentials(self, storage) -> None:
        test_name = "healthcheck/sikuliah.txt"
        try:
            saved = storage.save(test_name, ContentFile(b"ok"))
            exists = storage.exists(saved)
            storage.delete(saved)
        except Exception as exc:  # noqa: BLE001
            raise CommandError(f"Kredensial/bucket bermasalah: {exc}") from exc

        if not exists:
            raise CommandError("Unggah berhasil tetapi objek tidak ditemukan. Periksa bucket.")

        self.stdout.write(
            self.style.SUCCESS(
                f"Bucket dapat ditulis dan dibaca. Endpoint: "
                f"{settings.AWS_S3_ENDPOINT_URL or 'AWS default'}, "
                f"bucket: {settings.AWS_STORAGE_BUCKET_NAME}."
            )
        )
