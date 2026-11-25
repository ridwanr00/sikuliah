# 08 — Matriks Keterlacakan Kebutuhan

Tujuan: membuktikan bahwa **setiap kebutuhan punya rancangan, implementasi, pengujian, dan
bukti**. Matriks ini juga alat kerja — perbarui setiap akhir siklus (lihat dokumen 05),
bukan hanya di akhir.

Aturan pengisian:
- Kolom *Kode/URL* diisi setelah implementasi (nama view atau path).
- Kolom *Bukti* diisi nama berkas screenshot di `screenshots/`.
- Status: `✅` terpenuhi & teruji · `🟡` terimplementasi, belum teruji formal ·
  `⬜` belum · `➖` di luar lingkup (harus ada alasan di SRS §6).

## 1. Kebutuhan fungsional

| FR | Use case | Rancangan terkait | Implementasi (view / URL / model) | TC | Bukti | Status |
|----|----------|-------------------|-----------------------------------|----|-------|--------|
| FR-01 Autentikasi & RBAC | UC-01 | Gambar 4.1, §5.2 | `accounts.views.LoginView` `/masuk`; `User.role`; `RoleRequiredMixin` | TC-01, TC-07 | `tc-01-login.png`, `tc-07-403.png` || ✅ |
| FR-02 Kelola pengguna | UC-02 | ERD `USER` | `accounts.views.UserListView` `/pengguna` | uji manual | `fr-02-pengguna.png` || 🟡 |
| FR-03 Kelola mata kuliah | UC-03 | ERD `COURSE` | `courses.views.CourseCreateView` `/mata-kuliah/baru` | uji manual | `fr-03-mk.png` || ✅ |
| FR-04 Enrollment & pencarian | UC-04 | ERD `ENROLLMENT`, §6.6 | `courses.views.enroll`, `CourseListView?q=` | TC-08 | `tc-08-kosong.png` || ✅ |
| FR-05 Materi | UC-05 | Gambar 4.2 (terkait), §6.3 | `materials.views.MaterialCreateView`, `download` | TC-02, TC-04, TC-07 | `tc-02-materi-dosen.png` || ✅ |
| FR-06 Kelola tugas | UC-06 | ERD `ASSIGNMENT` | `assignments.views.AssignmentCreateView` | TC-05 | `tc-05-tenggat.png` || ✅ |
| FR-07 Pengumpulan tugas | UC-07 | Gambar 4.2, 4.5, §6.4 | `assignments.views.submit` `/tugas/<id>/kumpulkan` | TC-03, TC-04, TC-05 | `tc-03-submit.png` || ✅ |
| FR-08 Penilaian & umpan balik | UC-08 | Gambar 4.3, ERD `SUBMISSION` | `assignments.views.grade` `/pengumpulan/<id>/nilai` | TC-06 | `tc-06-nilai-dosen.png` || ✅ |
| FR-09 Pengumuman | UC-09 | ERD `ANNOUNCEMENT` | `announcements.views.CreateView` | uji manual | `fr-09-pengumuman.png` || 🟡 |
| FR-10 Statistik | UC-10 | §1 arsitektur, ERD agregat | `dashboard.views.statistics`, Chart.js | cocokkan manual | `fr-10-statistik.png` || ✅ |

## 2. Kebutuhan nonfungsional

| NFR | Cara dibuktikan | Lokasi bukti | Status |
|-----|-----------------|--------------|--------|
| NFR-01 Kinerja | 3× pengukuran DevTools | tabel §5 dok. 07 || 🟡 |
| NFR-02 Keamanan | Hash + CSRF + validasi unggah | tinjauan `settings.py`, `forms.py`; TC-04/07 || ✅ |
| NFR-03 Sesi | Uji diam 61 menit | tabel §5 dok. 07 || 🟡 |
| NFR-04 Kegunaan | Uji 3 orang, catat waktu | tabel §5 dok. 07 || 🟡 |
| NFR-05 Kompatibilitas | 3 peramban × 3 lebar layar | `tc-08-360px.png` + tabel || ✅ |
| NFR-06 Keandalan data | Constraint unik, transaksi | `models.py`, `migrations/` || ✅ |
| NFR-07 Keterpeliharaan | `ruff check`, struktur MVT | lampiran kode + hasil lint || ✅ |
| NFR-08 Halaman error | 403/404/500 kustom | `tc-07-403.png`, `tc-08-404.png` || ✅ |
| NFR-09 Aksesibilitas | Tab navigation, kontras | tabel §5 dok. 07 || 🟡 |
| NFR-10 Portabilitas | Jalankan di 2 mesin | catatan uji instalasi || 🟡 |

## 3. Keterlacakan balik (kode → kebutuhan)

Bagian ini mencegah "fitur yatim" — fitur yang ada di aplikasi tetapi tidak ada di SRS.
Untuk setiap aplikasi Django, isi tabel berikut setelah implementasi.

| Aplikasi Django | Model | View utama | FR yang dilayani |
|-----------------|-------|------------|------------------|
| `accounts` | User | login/logout, user CRUD | FR-01, FR-02 |
| `courses` | Course, Enrollment | course CRUD, enroll, detail | FR-03, FR-04 |
| `materials` | Material | materi CRUD, download | FR-05 |
| `assignments` | Assignment, Submission | tugas CRUD, submit, grade | FR-06, FR-07, FR-08 |
| `announcements` | Announcement | pengumuman CRUD | FR-09 |
| `dashboard` | — (agregasi) | dasbor, statistik | FR-10 |

> **TODO:** setelah coding, jalankan audit: buka setiap URL di `urls.py` dan pastikan ada
> baris di tabel ini. URL tanpa FR = fitur harus dihapus atau SRS diperbarui.

## 4. Ringkasan cakupan

| Ukuran | Target | Aktual |
|--------|--------|--------|
| FR terimplementasi / total | 10/10 | 10/10 |
| FR teruji formal (TC) / total | 10/10 | 8/10 (FR-02 & FR-09 uji manual) |
| NFR dibuktikan / total | 10/10 | 5/10 penuh, 5/10 sebagian |
| TC lulus / total | 8/8 | 8/8 |

> Angka inilah yang dikutip di kesimpulan PDF. Jangan menulis "semua kebutuhan terpenuhi"
> tanpa tabel ini terisi.
