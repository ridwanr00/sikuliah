# 07 — Rencana dan Hasil Pengujian

Brief mewajibkan **minimal 5 skenario** yang mencakup fitur utama, validasi input,
interaksi pengguna, dan kondisi kesalahan — diuji pada aplikasi yang benar-benar berjalan.

**Status eksekusi:** seluruh 8 test case di bawah sudah dijalankan pada aplikasi
(`python manage.py runserver`) pada 25 November 2026. Hasil aktual diisi berdasarkan
pengamatan langsung, bukan perkiraan.

| Ringkasan | Nilai |
|-----------|-------|
| Test case manual | 8 (TC-01 … TC-08) |
| Status | 8 Lulus / 0 Gagal |
| Pengujian otomatis Django | 13 test, 13 lulus (`python manage.py test`) |
| Pemeriksaan integrasi tambahan | 15 pemeriksaan (login, RBAC, unggah, unduh, penilaian) |
| Bug ditemukan & diperbaiki | 3 (lihat §6) |

---

## 1. Strategi pengujian

| Jenis | Sasaran | Cara |
|-------|---------|------|
| Fungsional | FR-01 … FR-10 berjalan sesuai kriteria penerimaan | TC manual + halaman aplikasi |
| Validasi input | Data kosong, format salah, ukuran berlebih, nilai di luar rentang | TC-04, TC-05, TC-06 |
| Otorisasi | Akses lintas peran dan lintas kepemilikan | TC-07 |
| Integrasi | Alur lintas tabel: unggah → simpan → tampil → nilai | TC-02, TC-03, TC-06 |
| Antarmuka/responsif | 390 px, 768 px, 1440 px | TC-08 + tabel NFR |
| Keadaan kesalahan | Pencarian kosong, 403, 404, 500 | TC-08 |
| Otomatis | Regresi alur tugas dan otorisasi | `python manage.py test` (13 test) |

**Tidak dilakukan:** uji beban, uji penetrasi, dan uji keamanan oleh pihak ketiga.
Dinyatakan sebagai keterbatasan di bab akhir PDF.

## 2. Lingkungan pengujian

| Item | Nilai |
|------|-------|
| Tanggal pengujian | 25 November 2026 |
| Perangkat | Laptop pribadi, RAM 8 GB |
| Sistem operasi | Linux (Ubuntu 24.04) |
| Python / Django | 3.12 / 5.2 |
| Basis data | SQLite 3 |
| Peramban | Chromium 159 (Playwright) dan Brave (mesin pengguna) |
| URL aplikasi | `http://127.0.0.1:8000` |
| Data uji | `python manage.py seed_demo` (kata sandi dari environment) | (35 pengguna, 6 mata kuliah, 24 materi, 12 tugas, 123 pengumpulan) |

### Akun uji

| Peran | Surel | Kata sandi | Catatan |
|-------|-------|------------|---------|
| Admin | admin@kampus.test | `DEMO_PASSWORD` (lihat `.env` lokal) | Panel `/admin` |
| Dosen | dosen1@kampus.test | `DEMO_PASSWORD` | Pengampu IF-301 dan IF-305 |
| Dosen lain | dosen2@kampus.test | `DEMO_PASSWORD` | Pengampu IF-302 (untuk uji 403) |
| Mahasiswa | mhs01@kampus.test | `DEMO_PASSWORD` | Terdaftar IF-301 |
| Mahasiswa non-peserta | mhs09@kampus.test | `DEMO_PASSWORD` | Tidak terdaftar di IF-301 |

## 3. Rekapitulasi

| TC | FR | Fokus | Status |
|----|----|-------|--------|
| TC-01 | FR-01 | Login valid dan tidak valid | ✅ Lulus |
| TC-02 | FR-05 | Unggah dan unduh materi (fitur utama 1) | ✅ Lulus |
| TC-03 | FR-07 | Pengumpulan tugas valid (fitur utama 2) | ✅ Lulus |
| TC-04 | FR-05/07 | Validasi berkas: ukuran dan ekstensi | ✅ Lulus |
| TC-05 | FR-06/07 | Penolakan pengumpulan setelah tenggat | ✅ Lulus |
| TC-06 | FR-08 | Validasi nilai dan umpan balik | ✅ Lulus |
| TC-07 | FR-01/05 | Otorisasi lintas peran dan kepemilikan | ✅ Lulus |
| TC-08 | FR-04 | Pencarian tanpa hasil + tampilan responsif | ✅ Lulus |

---

## 4. Detail test case

### TC-01 — Login valid dan tidak valid
| Field | Isi |
|-------|-----|
| **Kebutuhan terkait** | FR-01 (AC-01.1, AC-01.2, AC-01.3) |
| **Prakondisi** | Akun dosen1, mhs01, dan mhs09 aktif; aplikasi berjalan |
| **Langkah** | 1. Buka `/masuk`. 2. Isi `dosen1@kampus.test` + kata sandi benar → Masuk. 3. Perhatikan halaman tujuan dan menu. 4. Logout. 5. Login dengan kata sandi salah. 6. Login sebagai mhs01, lalu akses `/admin/`. |
| **Hasil yang diharapkan** | Langkah 2 → dasbor dosen, menu Dosen tampil. Langkah 5 → tetap di halaman login, pesan "Surel atau kata sandi tidak sesuai", tidak ada sesi. Langkah 6 → ditolak (tidak ada akses panel admin). |
| **Hasil aktual** | Login benar → 302 ke `/dasbor/`, nama "Anas Nasrulloh" dan badge Dosen tampil. Login salah → halaman login dengan pesan generik, sesi tidak dibuat. Mahasiswa → 403 saat membuka area admin. |
| **Status** | ✅ Lulus |
| **Bukti** | `screenshots/09-403.png`; uji otomatis `courses.tests.CourseAccessTests` |

### TC-02 — Unggah dan unduh materi
| Field | Isi |
|-------|-----|
| **Kebutuhan terkait** | FR-05 (AC-05.1, AC-05.5) |
| **Prakondisi** | Login dosen1, pengampu IF-301; data seeder berisi 4 materi |
| **Langkah** | 1. Buka IF-301 → bagian Materi. 2. Tambah materi "Uji Materi", pertemuan 5, unggah PDF. 3. Simpan. 4. Login mhs01 → buka IF-301 → Materi. 5. Klik Unduh. 6. Bandingkan berkas hasil unduh dengan berkas asli. |
| **Hasil yang diharapkan** | Materi muncul dengan pertemuan 5. Mahasiswa dapat mengunduh; isi berkas identik. |
| **Hasil aktual** | Materi tersimpan dan tampil terurut pertemuan. Unduhan mengembalikan HTTP 200, `Content-Disposition: attachment`, dan isi berkas identik byte-per-byte dengan berkas tersimpan (`identik: True`). |
| **Status** | ✅ Lulus |
| **Bukti** | `screenshots/02-materi-dosen.png`, `screenshots/03-materi-mahasiswa.png` |

### TC-03 — Pengumpulan tugas valid
| Field | Isi |
|-------|-----|
| **Kebutuhan terkait** | FR-07 (AC-07.1, AC-07.3) |
| **Prakondisi** | Login mhs01; tugas "Tugas 2" pada IF-301 belum lewat tenggat |
| **Langkah** | 1. Buka tugas. 2. Kumpulkan `jawaban.pdf`. 3. Catat waktu yang tampil. 4. Unggah ulang `jawaban-revisi.pdf`. 5. Buka halaman tugas lagi. 6. Periksa daftar pengumpulan di akun dosen. |
| **Hasil yang diharapkan** | Status "Terkumpul" dengan waktu server. Setelah unggah ulang, hanya satu baris pengumpulan berisi berkas terbaru. |
| **Hasil aktual** | Pengumpulan pertama tersimpan dengan waktu server. Unggahan kedua menggantikan berkas pada baris yang sama (jumlah record tetap 1); dosen melihat satu baris per mahasiswa. |
| **Status** | ✅ Lulus |
| **Bukti** | `screenshots/04-submit-tugas.png`, `screenshots/05-daftar-pengumpulan.png`; uji otomatis `test_unggah_ulang_tidak_menduplikasi` |

### TC-04 — Validasi berkas (ukuran dan ekstensi)
| Field | Isi |
|-------|-----|
| **Kebutuhan terkait** | FR-05/FR-07 (AC-05.2, AC-05.3, AC-07.4), BR-05 |
| **Prakondisi** | Login dosen1 dan mhs01; tersedia `besar.pdf` 6 MB dan `program.exe` |
| **Langkah** | 1. Dosen unggah berkas 6 MB sebagai materi. 2. Dosen unggah `program.exe`. 3. Mahasiswa unggah `program.exe` sebagai jawaban tugas. 4. Mahasiswa unggah berkas 0 byte. |
| **Hasil yang diharapkan** | Semua ditolak dengan pesan spesifik; tidak ada record atau berkas baru tersimpan. |
| **Hasil aktual** | Berkas 6 MB → "Ukuran berkas maksimum 5 MB". `.exe` → "Format .exe tidak diizinkan. Gunakan: docx, pdf, pptx, zip." Berkas 0 byte → "Berkas kosong (0 byte)". Jumlah materi IF-301 tetap 4 (tidak ada record baru). |
| **Status** | ✅ Lulus |
| **Bukti** | `screenshots/08-validasi-error.png`; uji otomatis `test_ekstensi_terlarang_ditolak` |

### TC-05 — Penolakan pengumpulan setelah tenggat
| Field | Isi |
|-------|-----|
| **Kebutuhan terkait** | FR-06/FR-07 (AC-06.1, AC-06.2, AC-07.2) |
| **Prakondisi** | Login dosen1; tugas "Tugas 1" pada IF-301 memiliki tenggat yang sudah lewat |
| **Langkah** | 1. Dosen mencoba membuat tugas dengan tenggat 2020-01-01. 2. Buka "Tugas 1" sebagai mhs01. 3. Coba kumpulkan berkas. |
| **Hasil yang diharapkan** | Langkah 1 → form ditolak. Langkah 2 → label "Lewat tenggat", form pengumpulan tidak tampil. Langkah 3 (bila dipaksa) → ditolak server, tidak ada record baru. |
| **Hasil aktual** | Form tugas menolak dengan pesan "Tenggat harus setelah waktu sekarang". Halaman tugas lewat tenggat menampilkan "Tenggat telah berakhir" tanpa form. Permintaan POST langsung ke URL pengumpulan ditolak; jumlah pengumpulan mhs01 tidak berubah. |
| **Status** | ✅ Lulus |
| **Bukti** | `screenshots/02-materi-dosen.png` (status pada daftar tugas); uji otomatis `test_pengumpulan_setelah_tenggat_ditolak` |

### TC-06 — Penilaian dan validasi nilai
| Field | Isi |
|-------|-----|
| **Kebutuhan terkait** | FR-08 (AC-08.1, AC-08.2, AC-08.3), BR-03 |
| **Prakondisi** | Ada pengumpulan mhs01 pada tugas bernilai maksimum 100 |
| **Langkah** | 1. Login dosen1 → tugas → daftar pengumpulan. 2. Isi nilai `101`. 3. Isi nilai `abc`. 4. Isi nilai `85` + umpan balik. 5. Login mhs01, buka halaman tugas. |
| **Hasil yang diharapkan** | Langkah 2–3 ditolak. Langkah 4 tersimpan dan status "Dinilai". Langkah 5 → nilai 85 dan umpan balik tampil. |
| **Hasil aktual** | Nilai 101 dan `abc` ditolak ("Nilai harus antara 0 dan 100"). Nilai 85 tersimpan dengan `graded_at`; mahasiswa melihat "85/100" dan umpan balik lengkap. Rekap menampilkan rata-rata dan jumlah dinilai. |
| **Status** | ✅ Lulus |
| **Bukti** | `screenshots/05-daftar-pengumpulan.png`, `screenshots/06-nilai-mahasiswa.png`; uji otomatis `test_nilai_di_luar_rentang_ditolak` |

### TC-07 — Otorisasi lintas peran dan kepemilikan
| Field | Isi |
|-------|-----|
| **Kebutuhan terkait** | FR-01 (AC-01.3), FR-05 (AC-05.4), FR-07 (AC-07.5), FR-08 |
| **Prakondisi** | Login mhs09 (tidak terdaftar IF-301) dan dosen2 (bukan pengampu IF-301) |
| **Langkah** | 1. mhs09 membuka `/mata-kuliah/1/` langsung dari URL. 2. mhs09 membuka URL unduhan materi IF-301. 3. dosen2 membuka halaman pengumpulan tugas dosen1. 4. Logout, lalu buka `/dasbor/`. |
| **Hasil yang diharapkan** | Langkah 1–3 → 403 dengan halaman kustom. Langkah 4 → diarahkan ke `/masuk/?next=/dasbor/`. |
| **Hasil aktual** | Ketiga akses mengembalikan 403 dan menampilkan halaman "Anda tidak memiliki akses ke halaman ini" berbahasa Indonesia. Tanpa login → redirect 302 ke halaman login dengan parameter `next`. |
| **Status** | ✅ Lulus |
| **Bukti** | `screenshots/09-403.png`; uji otomatis `CourseAccessTests` dan `test_dosen_lain_tidak_dapat_menilai` |

### TC-08 — Pencarian tanpa hasil dan tampilan responsif
| Field | Isi |
|-------|-----|
| **Kebutuhan terkait** | FR-04 (AC-04.3), NFR-05, NFR-08 |
| **Prakondisi** | Login mhs01 |
| **Langkah** | 1. Buka daftar mata kuliah, cari "zzz". 2. Buka lebar jendela 390 px, buka halaman mata kuliah. 3. Ulangi pada 768 px dan 1440 px. 4. Buka URL `/tidak-ada/`. |
| **Hasil yang diharapkan** | Langkah 1 → pesan kosong informatif. Langkah 2–3 → navigasi dapat dipakai, tidak ada konten terpotong. Langkah 4 → halaman 404 kustom. |
| **Hasil aktual** | Pencarian "zzz" → "Tidak ada mata kuliah yang cocok dengan "zzz"". Pada 390 px tabel materi menyesuaikan (kolom berkas disembunyikan) dan tombol tetap utuh; navbar berubah menjadi menu lipat. 404 kustom tampil. |
| **Status** | ✅ Lulus |
| **Bukti** | `screenshots/10-responsif-360px.png` |

---

## 5. Pemeriksaan nonfungsional (pendukung)

| NFR | Cara uji | Ambang | Hasil |
|-----|----------|--------|-------|
| NFR-01 Kinerja | Muat ulang dasbor 3× di lokal | < 3 detik | ✅ 0,2–0,5 detik (lokal, data demo) |
| NFR-02 Keamanan | Periksa hash kata sandi; POST tanpa token CSRF | Hash bukan teks asli; POST ditolak | ✅ PBKDF2; POST tanpa CSRF → 403 |
| NFR-03 Sesi | Diamkan 61 menit | Diarahkan ke login | 🟡 belum diuji (menunggu waktu) |
| NFR-04 Kegunaan | Uji coba alur submit | ≤ 3 menit | 🟡 belum diuji formal |
| NFR-05 Kompatibilitas | 390/768/1440 px, Chromium | Tidak ada konten terpotong | ✅ |
| NFR-06 Keandalan data | Constraint unik + uji unggah ulang | Tidak ada duplikat | ✅ 1 record per (tugas, mahasiswa) |
| NFR-07 Keterpeliharaan | `ruff check src` | Tidak ada temuan | ✅ All checks passed |
| NFR-08 Halaman error | 403/404 kustom | Tampil berbahasa Indonesia | ✅ |
| NFR-09 Aksesibilitas | Label, kontras, navigasi | Standar dasar | 🟡 sebagian (label & kontras ok, uji keyboard belum formal) |
| NFR-10 Portabilitas | Instalasi ulang di mesin lain | README dapat diikuti | 🟡 belum diuji di Windows |

## 6. Bug log (temuan nyata selama pengembangan)

| Bug | TC | Gejala | Penyebab | Perbaikan | Uji ulang | Status |
|-----|----|--------|----------|-----------|-----------|--------|
| BUG-01 | TC-04 | Pesan "Isi salah satu…" muncul dua kali di form materi | Validasi yang sama dilakukan di `MaterialForm.clean()` dan `Material.clean()` | Hapus validasi ganda di form, sisakan di model | TC-04 lulus, pesan tunggal | ✅ |
| BUG-02 | Statistik | Tingkat pengumpulan dosen tampil 30% padahal data ~74% | Target dihitung `total peserta × total tugas`, padahal tiap mata kuliah punya peserta dan tugas berbeda | Hitung `Σ(peserta mata kuliah × jumlah tugas mata kuliah)` | Dasbor menunjukkan 74% (61/82) | ✅ |
| BUG-03 | TC-08 | Tombol "Unduh" terpotong pada layar 390 px | Kolom berkas + tiga tombol aksi memaksa lebar tabel melebihi layar | Sembunyikan kolom berkas di layar kecil, tombol menumpuk vertikal | Screenshot 390 px tanpa clipping | ✅ |

## 7. Kriteria keluar (exit criteria)

Pengujian dianggap selesai bila:
1. 8 TC dieksekusi pada aplikasi berjalan — ✅ terpenuhi.
2. Tidak ada TC berstatus Gagal tanpa catatan penyebab dan perbaikan — ✅ terpenuhi.
3. Screenshot bukti tersimpan dengan nama sesuai dokumen 10 — ✅ 10 berkas.
4. Matriks keterlacakan diperbarui — ✅ dokumen 08.
5. Rekap angka dimasukkan ke PDF — ✅ 8/8 lulus.
