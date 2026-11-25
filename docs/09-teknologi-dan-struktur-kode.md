# 09 — Teknologi, Struktur Kode, dan Konvensi

Dokumen ini menjawab dua item penilaian sekaligus: **alasan pemilihan teknologi** dan
**struktur source code yang terorganisasi, mudah dipelihara, serta menjaga konfigurasi
sensitif**.

---

## 1. Tumpukan teknologi

| Lapis | Teknologi | Versi | Peran |
|-------|-----------|-------|-------|
| Bahasa | Python | 3.12 | Seluruh logika aplikasi |
| Framework | Django | 5.2 LTS | Routing, ORM, autentikasi, form, template |
| Basis data | SQLite 3 (dev) / MySQL 8 (opsional) | — | Penyimpanan data |
| Antarmuka | Django Templates + Bootstrap 5.3 (disimpan lokal) | — | Halaman responsif tanpa build step |
| Grafik | Chart.js 4 | — | Dasbor statistik (FR-10) |
| Berkas | Django `FileField` + `media/` | — | Materi & pengumpulan |
| Konfigurasi | `python-decouple` + `.env` | — | Memisahkan rahasia dari kode |
| Kualitas kode | `ruff` | — | Lint dan format |
| Pengujian | `TestCase` Django (otomatis) + TC manual | — | Verifikasi FR |
| Kontrol versi | Git + GitHub | — | Riwayat, kolaborasi |

### 1.1 Alasan pemilihan

1. **Django vs Flask** — Flask minimal dan menyenangkan, tetapi autentikasi, sesi, form,
   validasi, migrasi, dan panel admin harus dirakit sendiri. Untuk brief yang menilai
   otorisasi peran dan validasi input, Django memberi semuanya secara bawaan sehingga
   waktu habis untuk fitur, bukan infrastruktur.
2. **Django vs FastAPI** — FastAPI unggul untuk API, tetapi proyek ini butuh render HTML
   sisi server, formulir, dan unggah berkas; template + form Django lebih langsung.
3. **Template Django vs SPA (React/Vue)** — tim kecil, tenggat pendek, dan tidak ada
   kebutuhan interaksi real-time. Menghindari dua basis kode (API + klien) mengurangi
   permukaan bug dan waktu setup.
4. **Bootstrap vs Tailwind** — Bootstrap tidak butuh Node/npm build; cukup satu tautan CSS
   (disimpan lokal agar demo tetap jalan tanpa internet). Konsistensi komponen lebih mudah
   dijamin untuk tim yang belum berpengalaman desain.
5. **SQLite vs MySQL** — SQLite cukup untuk demo dan memudahkan penilai menjalankan proyek
   tanpa instalasi server DB. MySQL disiapkan sebagai opsi melalui variabel lingkungan.
6. **Alasan keamanan** — Django menyediakan proteksi CSRF, escaping template (XSS),
   password hashing PBKDF2, dan query ORM berparameter secara bawaan. Ini menjawab NFR-02
   tanpa menulis lapisan keamanan sendiri.

---

## 2. Struktur proyek

```
src/
├── manage.py
├── requirements.txt
├── .env.example
├── config/                     # konfigurasi proyek
│   ├── settings.py
│   ├── urls.py
│   ├── wsgi.py / asgi.py
├── apps/
│   ├── accounts/               # FR-01, FR-02
│   │   ├── models.py           # User(AbstractUser) + role
│   │   ├── forms.py
│   │   ├── views.py
│   │   ├── urls.py
│   │   ├── mixins.py           # RoleRequiredMixin
│   │   ├── migrations/
│   │   └── tests.py
│   ├── courses/                # FR-03, FR-04
│   ├── materials/              # FR-05
│   ├── assignments/            # FR-06, FR-07, FR-08
│   ├── announcements/          # FR-09
│   └── dashboard/              # FR-10
├── templates/
│   ├── base.html               # navbar, footer, blok pesan
│   ├── components/             # _card.html, _empty_state.html, _pagination.html
│   ├── accounts/
│   ├── courses/
│   ├── materials/
│   ├── assignments/
│   ├── dashboard/
│   └── errors/                 # 403.html, 404.html, 500.html
├── static/
│   ├── css/custom.css
│   ├── js/chart.min.js
│   └── vendor/bootstrap/
├── media/                      # TIDAK di-commit
│   ├── materials/
│   └── submissions/
└── seed/                       # perintah seed_demo
```

**Aturan struktur:**
- Satu aplikasi Django = satu domain kebutuhan; jangan menaruh view materi di `courses`.
- Template mengikuti nama aplikasi; komponen berulang diawali `_`.
- Tidak ada logika bisnis di template; tidak ada query mentah di view bila ORM cukup.
- `media/` dan `.env` masuk `.gitignore`.

---

## 3. Konvensi penamaan

| Objek | Konvensi | Contoh |
|-------|----------|--------|
| Model | PascalCase, tunggal | `Submission`, `Announcement` |
| Field | snake_case | `submitted_at`, `max_score` |
| View | PascalCase + `View` / fungsi kata kerja | `MaterialCreateView`, `submit_assignment` |
| URL name | kata benda + aksi | `material_list`, `assignment_submit` |
| Path URL | bahasa Indonesia, kebab-case, diakhiri `/` | `/mata-kuliah/<id>/materi/` |
| Template | snake_case | `assignment_detail.html` |
| Variabel konteks | snake_case, jelas | `submissions`, `is_late` |
| Berkas unggahan | nama acak + ekstensi asli | `materials/2025/10/a1b2c3.pdf` |
| Konstanta | UPPER_SNAKE | `MAX_UPLOAD_SIZE`, `ALLOWED_EXTENSIONS` |

---

## 4. Penanganan kesalahan

| Lapis | Aturan |
|-------|--------|
| Form | Validasi di `forms.py`; pesan bahasa Indonesia; tampilkan per field + ringkasan |
| View | Cek otorisasi sebelum query; `get_object_or_404` untuk objek; `PermissionDenied` (403) untuk pelanggaran peran |
| Berkas | Validasi ekstensi, MIME (`content_type`), ukuran, dan isi tidak kosong; simpan nama acak |
| Global | `handler403/404/500` mengarah ke template kustom; `DEBUG=False` untuk demo publik |
| Log | `logging` ke konsol saat dev; jangan mencatat kata sandi atau isi berkas |

Prinsip: **pesan error memberi tahu apa yang salah dan apa langkah berikutnya**, tanpa
membocorkan detail internal (stack trace, query SQL, path server).

---

## 5. Pengelolaan konfigurasi sensitif

`.env.example` (di-commit):

```env
DJANGO_SECRET_KEY=ganti-dengan-nilai-acak
DJANGO_DEBUG=True
DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
DATABASE_URL=sqlite:///db.sqlite3
MAX_UPLOAD_SIZE_MB=5
```

Aturan:
1. `.env` **tidak pernah** di-commit; `.gitignore` memuat `.env`, `*.sqlite3`, `media/`.
2. `SECRET_KEY`, kredensial DB, dan kunci pihak ketiga hanya dibaca dari lingkungan.
3. Sebelum menyerahkan ZIP: `git log -p | grep -i "secret\|password"` untuk memastikan
   tidak ada rahasia di riwayat.
4. Kata sandi akun demo didokumentasikan di README **hanya** untuk lingkungan lokal, dan
   diberi peringatan agar diganti bila aplikasi dipublikasikan.

---

## 6. Alur kerja Git

| Branch | Fungsi |
|--------|--------|
| `main` | Versi stabil yang didemokan |
| `dev` | Integrasi harian |
| `feat/<fitur>` | Satu fitur/fungsi |

Format commit: `tipe(lingkup): ringkasan`
Contoh: `feat(materi): validasi ekstensi dan ukuran berkas`,
`fix(tugas): cegah pengumpulan ganda`, `docs(srs): bekukan ID kebutuhan v1.0`.

Aturan: setiap PR minimal ditinjau satu anggota; tidak ada commit berisi `.env`, `db.sqlite3`,
atau `media/`.

---

## 7. Cara menjalankan (ringkas — detail di README)

```bash
python -m venv .venv
source .venv/bin/activate        # Windows: .venv\Scripts\activate
pip install -r requirements.txt
cp .env.example .env             # isi SECRET_KEY
python manage.py migrate
python manage.py seed_demo       # data contoh
python manage.py runserver
```

Buka `http://127.0.0.1:8000`.

---

## 8. Dependensi awal (`requirements.txt`)

```text
asgiref==3.13.0
django==5.2.19
python-decouple==3.8
ruff==0.17.6
sqlparse==0.6.1
whitenoise==6.12.0
```

Daftar di atas adalah hasil `uv pip freeze` pada lingkungan yang benar-benar dipakai.
Tidak ada paket yang hanya terpasang untuk eksperimen.

---

## 9. Kesiapan demonstrasi

| Kebutuhan | Tindakan |
|-----------|----------|
| Tanpa internet | Bootstrap (CSS+JS) dan Chart.js disimpan di `static/vendor/` |
| Data selalu ada | `seed_demo` idempoten (aman dijalankan berulang) |
| Waktu tenggat | Sediakan satu tugas dengan tenggat +3 hari dan satu yang sudah lewat |
| Akun | Satu akun per peran, kata sandi demo |
| Reset cepat | `rm db.sqlite3 && python manage.py migrate && python manage.py seed_demo` |
