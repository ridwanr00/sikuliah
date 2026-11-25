# SIKULIAH — Learning Management System Kampus

Aplikasi web untuk mengelola perkuliahan satu program studi: distribusi materi, pengumpulan
dan penilaian tugas, pengumuman, serta statistik perkuliahan. Dibangun dengan **Python +
Django** sebagai tugas kelompok mata kuliah Rekayasa Perangkat Lunak.

> **Status:** aplikasi sudah diimplementasikan dan diuji pada 25 November 2026
> (13 pengujian otomatis lulus, 8 test case manual lulus). Struktur folder di bawah
> adalah struktur nyata, bukan rencana.

| Item | Keterangan |
|------|------------|
| Nama aplikasi | SIKULIAH |
| Kelompok | Kelompok 22 |
| Anggota | Ridwan Rasyid (1003260037) — dikerjakan mandiri |
| Mata kuliah | Rekayasa Perangkat Lunak |
| Institusi | Institut Teknologi Tangerang Selatan |

---

## 1. Fitur utama

| Fitur | Peran | Kebutuhan |
|-------|-------|-----------|
| Login & hak akses berbasis peran | Semua | FR-01 |
| Kelola pengguna | Admin | FR-02 |
| Kelola mata kuliah & enrollment | Admin, Dosen, Mahasiswa | FR-03, FR-04 |
| **Materi pembelajaran** (unggah, unduh, validasi berkas) | Dosen, Mahasiswa | FR-05 |
| **Tugas & pengumpulan daring** (tenggat, unggah ulang) | Dosen, Mahasiswa | FR-06, FR-07 |
| **Penilaian & umpan balik** | Dosen, Mahasiswa | FR-08 |
| Pengumuman mata kuliah | Dosen, Mahasiswa | FR-09 |
| Dasbor statistik (peserta, tingkat pengumpulan, distribusi nilai) | Admin, Dosen | FR-10 |

Rincian kebutuhan, diagram, dan kriteria penerimaan ada di folder [`docs/`](docs/README.md).

## 2. Teknologi

| Komponen | Teknologi |
|----------|-----------|
| Bahasa | Python 3.12 |
| Framework | Django 5.2 |
| Basis data | SQLite (pengembangan) / MySQL 8 (opsional) |
| Antarmuka | Django Templates, Bootstrap 5.3 (lokal), Chart.js |
| Grafik | Chart.js 4 |
| Berkas | Django `FileField` (`media/`) |

Alasan pemilihan teknologi: [`docs/09-teknologi-dan-struktur-kode.md`](docs/09-teknologi-dan-struktur-kode.md).

## 3. Struktur folder

```text
.
├── README.md
├── requirements.txt
├── .env.example
├── pyproject.toml         # konfigurasi ruff (lint)
├── docs/                  # SRS, rancangan, pengujian, build PDF
│   └── build/             # Dokumentasi-Proyek.pdf
├── screenshots/           # bukti implementasi (10 gambar)
└── src/                   # proyek Django
    ├── manage.py
    ├── config/            # settings, urls
    ├── apps/              # accounts, courses, materials, assignments, announcements, dashboard
    ├── templates/
    ├── static/
    └── media/             # tidak di-commit
```

> **TODO:** sesuaikan bila nama folder berubah saat implementasi. Struktur di README harus
> sama dengan struktur nyata.

## 4. Persyaratan

- Python 3.11 atau lebih baru (diuji pada 3.12)
- `pip` dan `venv`
- Git (opsional, untuk kloning)
- Peramban modern: Chrome, Edge, atau Firefox
- Tidak perlu Node.js atau server basis data untuk mode SQLite

## 5. Instalasi

```bash
git clone [URL-REPOSITORI]
cd [nama-folder]
python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate
pip install -r requirements.txt
```

## 6. Konfigurasi

```bash
cp .env.example .env
```

Isi nilai pada `.env`:

| Variabel | Contoh | Keterangan |
|----------|--------|------------|
| `DJANGO_SECRET_KEY` | `ganti-dengan-string-acak` | Wajib; jangan dibagikan |
| `DJANGO_DEBUG` | `True` | `False` untuk demo publik |
| `DJANGO_ALLOWED_HOSTS` | `127.0.0.1,localhost` | Pisahkan dengan koma |
| `DATABASE_URL` | `sqlite:///db.sqlite3` | Kosongkan untuk SQLite default |
| `MAX_UPLOAD_SIZE_MB` | `5` | Batas ukuran unggahan |

Membuat `SECRET_KEY` baru:

```bash
python -c "from django.core.management.utils import get_random_secret_key as g; print(g())"
```

## 7. Menjalankan aplikasi

```bash
cd src
python manage.py migrate
python manage.py seed_demo          # data contoh: dosen, mahasiswa, mata kuliah, tugas
python manage.py runserver
```

Buka <http://127.0.0.1:8000>.

### Akun demo

| Peran | Surel | Kata sandi |
|-------|-------|------------|
| Admin | admin@kampus.test | `admin12345` |
| Dosen | dosen1@kampus.test | `dosen12345` |
| Mahasiswa | mhs1@kampus.test | `mhs12345` |

> Kata sandi di atas hanya untuk lingkungan lokal/demo. Ganti bila aplikasi dipublikasikan.

## 8. Cara menggunakan

1. **Dosen** — masuk → pilih mata kuliah → tab *Materi* → *Tambah materi* (PDF/DOCX/PPTX/ZIP,
   maks. 5 MB) → tab *Tugas* → *Buat tugas* (tenggat & nilai maksimum) → buka tugas →
   *Pengumpulan* → beri nilai dan umpan balik.
2. **Mahasiswa** — masuk → *Mata Kuliah* → daftar → buka mata kuliah → unduh materi →
   buka tugas → *Kumpulkan* sebelum tenggat → lihat nilai setelah dinilai.
3. **Admin** — masuk → *Pengguna* untuk mengelola akun → *Mata Kuliah* untuk membuat mata
   kuliah dan menetapkan dosen.

## 9. Pengujian

```bash
source .venv/bin/activate        # bila belum aktif
cd src
python manage.py test            # 13 test otomatis
cd .. && ruff check src          # lint
```

Hasil terakhir:

| Pemeriksaan | Hasil |
|-------------|-------|
| `manage.py test` | 13 test, semuanya lulus |
| `ruff check src` | tidak ada temuan |
| Test case manual TC-01…TC-08 | 8/8 lulus |
| Pemeriksaan integrasi (login, RBAC, unggah/unduh, penilaian) | 15/15 lulus |

Skenario manual, hasil aktual, dan bug log:
[`docs/07-rencana-dan-hasil-pengujian.md`](docs/07-rencana-dan-hasil-pengujian.md).
Bukti tangkapan layar ada di [`screenshots/`](screenshots/).

## 10. Bukti implementasi

| Berkas | Isi |
|--------|-----|
| `screenshots/01-beranda.png` | Halaman utama |
| `screenshots/02-materi-dosen.png` | Fitur utama 1 — kelola materi |
| `screenshots/03-materi-mahasiswa.png` | Mahasiswa mengunduh materi |
| `screenshots/04-submit-tugas.png` | Fitur utama 2 — form pengumpulan |
| `screenshots/05-daftar-pengumpulan.png` | Daftar pengumpulan dosen |
| `screenshots/06-nilai-mahasiswa.png` | Nilai dan umpan balik |
| `screenshots/07-statistik.png` | Dasbor statistik |
| `screenshots/08-validasi-error.png` | Validasi berkas |
| `screenshots/09-403.png` | Otorisasi lintas peran |
| `screenshots/10-responsif-360px.png` | Tampilan 390 px |

## 11. Penanganan masalah umum

| Gejala | Penyebab | Solusi |
|--------|----------|--------|
| `ModuleNotFoundError: django` | Virtual environment belum aktif | `source .venv/bin/activate` lalu `pip install -r requirements.txt` |
| `no such table: ...` | Migrasi belum dijalankan | `python manage.py migrate` |
| Halaman kosong / tidak ada data | Seeder belum dijalankan | `python manage.py seed_demo` |
| `CSRF verification failed` | Cookie/izin peramban | Muat ulang halaman; pastikan `CSRF_TRUSTED_ORIGINS` sesuai host |
| Unggahan ditolak | Ekstensi/ukuran tidak sesuai | Gunakan PDF/DOCX/PPTX/ZIP ≤ 5 MB |
| `Error: That port is already in use` | Server lain di port 8000 | `python manage.py runserver 8001` |
| Gaya CSS tidak muncul | `DEBUG=False` tanpa static server | Jalankan `collectstatic` atau set `DEBUG=True` untuk demo lokal |
| Data ingin direset | Basis data uji kotor | `rm db.sqlite3 && python manage.py migrate && python manage.py seed_demo` |

## 12. Keterbatasan

- Satu dosen pengampu per mata kuliah; belum ada tim pengajar.
- Tanpa integrasi SIAKAD, notifikasi surel, atau aplikasi mobile.
- Berkas disimpan di sistem berkas lokal, bukan object storage.
- Statistik hanya dari data aplikasi (data demo pada versi ini), bukan data akademik resmi.
- Belum diuji beban atau diaudit keamanannya secara independen.

## 13. Lisensi dan penggunaan data

Proyek ini dibuat untuk keperluan akademik. Data yang disertakan adalah data sintetis;
jangan menggunakan data mahasiswa nyata tanpa izin.
