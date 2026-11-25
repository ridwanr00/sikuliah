# 03 — Software Requirements Specification (SRS)

**Proyek:** SIKULIAH — Learning Management System Kampus
**Versi:** 1.0 · **Tanggal:** 25 November 2026
**Disusun oleh:** Ridwan Rasyid (1003260037) — Kelompok 22
**Mengacu pada:** struktur IEEE 830 (disederhanakan)

---

## 1. Pendahuluan

### 1.1 Tujuan dokumen
Dokumen ini menetapkan kebutuhan perangkat lunak SIKULIAH secara lengkap dan dapat diuji.
Dokumen menjadi dasar tunggal bagi perancangan (dokumen 04), implementasi, dan pengujian
(dokumen 07). Setiap kebutuhan memiliki ID unik yang dipakai kembali di matriks
keterlacakan (dokumen 08).

### 1.2 Ruang lingkup produk
SIKULIAH adalah aplikasi web berbasis Python/Django untuk mengelola perkuliahan satu
program studi: distribusi materi, pengelolaan tugas, pengumpulan berkas, penilaian,
pengumuman, dan statistik perkuliahan. Produk berjalan di peramban, bukan aplikasi mobile.

### 1.3 Definisi dan akronim
Lihat [01 — Latar Belakang §6](01-latar-belakang-dan-tujuan.md). Tambahan:

| Istilah | Arti |
|---------|------|
| RBAC | Role-Based Access Control |
| CSRF | Cross-Site Request Forgery |
| ORM | Object-Relational Mapping |
| TTFB | Time To First Byte |
| MVT | Model-View-Template (pola arsitektur Django) |

### 1.4 Referensi
1. IEEE Std 830-1998, *Recommended Practice for Software Requirements Specifications*.
2. Sommerville, I. *Software Engineering*, 10th ed.
3. Dokumentasi Django 5.2 — https://docs.djangoproject.com/en/5.2/
4. Dokumen internal: 01, 02, 04, 05, 06.

### 1.5 Ikhtisar dokumen
Bab 2 menjelaskan konteks produk. Bab 3–5 memuat kebutuhan fungsional, nonfungsional, dan
data. Bab 6 menetapkan batasan eksplisit. Bab 7 memuat matriks keterlacakan ringkas.

---

## 2. Deskripsi umum

### 2.1 Perspektif produk
SIKULIAH adalah produk baru (greenfield), berdiri sendiri, dan tidak terintegrasi dengan
sistem akademik kampus. Data pengguna dibuat oleh admin atau didaftarkan sendiri (self
registration khusus mahasiswa dengan verifikasi NIM sederhana). Sistem berjalan sebagai
aplikasi web tiga lapis:

```
Peramban  →  Aplikasi Django (URL router, view, template)  →  Basis data + penyimpanan berkas
```

### 2.2 Fungsi utama produk

| No | Fungsi | FR terkait | Fitur utama? |
|----|--------|------------|--------------|
| 1 | Autentikasi dan otorisasi peran | FR-01 | pendukung |
| 2 | Pengelolaan pengguna | FR-02 | pendukung |
| 3 | Pengelolaan mata kuliah | FR-03 | pendukung |
| 4 | Pendaftaran mata kuliah | FR-04 | pendukung |
| 5 | Materi pembelajaran | FR-05 | **ya (1)** |
| 6 | Pengelolaan tugas | FR-06 | **ya (2)** |
| 7 | Pengumpulan tugas | FR-07 | **ya (2)** |
| 8 | Penilaian dan umpan balik | FR-08 | **ya (2)** |
| 9 | Pengumuman | FR-09 | pendukung |
| 10 | Dasbor statistik | FR-10 | pendukung (bahan video) |

### 2.3 Karakteristik pengguna
Lihat [02 §2](02-stakeholder-dan-hak-akses.md). Diasumsikan seluruh pengguna mampu
mengoperasikan peramban modern dan mengunggah berkas.

### 2.4 Lingkungan operasi
- Server: Python 3.12, Django 5.2, SQLite (pengembangan) / MySQL 8 (opsional).
- Klien: Chrome, Edge, Firefox versi terbaru; lebar layar 360 px–1920 px.
- Zona waktu `Asia/Jakarta`, bahasa antarmuka Indonesia.

### 2.5 Batasan desain dan implementasi
- BR-01: satu mata kuliah memiliki tepat satu dosen pengampu pada versi ini.
- BR-02: satu mahasiswa hanya boleh memiliki satu pengumpulan aktif per tugas; pengumpulan
  ulang menggantikan berkas sebelumnya selama belum dinilai dan belum lewat tenggat.
- BR-03: nilai berada pada rentang 0 sampai nilai maksimum tugas (0–100).
- BR-04: tenggat tugas tidak boleh lebih awal dari waktu pembuatan.
- BR-05: berkas yang diterima: PDF, DOCX, ZIP; maksimum 5 MB per berkas.
- BR-06: akun nonaktif tidak dapat login, tetapi datanya tetap tersimpan.

### 2.6 Asumsi dan dependensi
- A-01: tersedia satu server lokal/layanan hosting gratis untuk demonstrasi.
- A-02: data awal (pengguna, mata kuliah) diisi melalui seeder untuk keperluan demo.
- A-03: tidak ada integrasi surel; notifikasi hanya di dalam aplikasi.
- A-04: dosen dan mahasiswa memiliki alamat surel aktif sebagai nama pengguna.

---

## 3. Kebutuhan fungsional

Format kriteria penerimaan memakai pola **Diberikan / Ketika / Maka** agar dapat langsung
diterjemahkan menjadi test case.

### FR-01 — Autentikasi dan otorisasi berbasis peran
- **Aktor:** semua pengguna · **Prioritas:** wajib
- **Deskripsi:** Sistem menyediakan login, logout, dan pembatasan akses berdasarkan peran
  (`admin`, `dosen`, `mahasiswa`). Setiap permintaan diverifikasi di sisi server.
- **Prakondisi:** akun terdaftar dan berstatus aktif.
- **Alur utama:** pengguna membuka halaman login → mengisi surel dan kata sandi → sistem
  memverifikasi → sistem mengarahkan ke dasbor sesuai peran.
- **Alur alternatif:** kredensial salah → pesan "Surel atau kata sandi tidak sesuai" tanpa
  mengungkap bagian mana yang salah; akun nonaktif → pesan "Akun tidak aktif, hubungi admin";
  pengguna belum login membuka halaman terbatas → diarahkan ke login dengan parameter
  `next`.
- **Kriteria penerimaan:**
  - AC-01.1 Diberikan kredensial valid, ketika login, maka sesi dibuat dan dasbor peran
    tampil dalam < 2 detik.
  - AC-01.2 Diberikan kredensial salah, ketika login, maka tetap di halaman login dan pesan
    error tampil; tidak ada sesi dibuat.
  - AC-01.3 Diberikan mahasiswa yang login, ketika membuka URL halaman admin, maka sistem
    mengembalikan 403 dan bukan halaman admin.
  - AC-01.4 Diberikan pengguna logout, ketika menekan tombol kembali di peramban, maka
    halaman terbatas tidak dapat ditampilkan dari cache.

### FR-02 — Pengelolaan pengguna oleh admin
- **Aktor:** admin · **Prioritas:** wajib
- **Deskripsi:** Admin dapat melihat daftar pengguna dengan pencarian dan filter peran,
  membuat akun, mengubah data, serta menonaktifkan akun.
- **Alur utama:** admin membuka menu Pengguna → tambah → mengisi nama, surel, NIM/NIDN,
  peran, kata sandi awal → simpan → akun muncul di daftar.
- **Alur alternatif:** surel sudah dipakai → pesan "Surel sudah terdaftar"; field wajib
  kosong → pesan per field; menonaktifkan akun sendiri → ditolak.
- **Kriteria penerimaan:**
  - AC-02.1 Akun baru dapat login dengan kata sandi awal dan langsung diminta menggantinya
    (opsional, boleh ditunda).
  - AC-02.2 Menonaktifkan akun membuat login akun tersebut gagal.
  - AC-02.3 Pencarian berdasarkan nama atau NIM mengembalikan hasil yang sesuai.
  - AC-02.4 Data historis (nilai, pengumpulan) akun nonaktif tetap ada.

### FR-03 — Pengelolaan mata kuliah
- **Aktor:** admin (buat/ubah/arsip), dosen (lihat miliknya) · **Prioritas:** wajib
- **Deskripsi:** Mata kuliah memiliki kode unik, nama, SKS, semester, tahun ajaran, dosen
  pengampu, dan deskripsi.
- **Kriteria penerimaan:**
  - AC-03.1 Kode mata kuliah duplikat ditolak dengan pesan yang menyebut kode tersebut.
  - AC-03.2 SKS hanya menerima bilangan 1–6.
  - AC-03.3 Mata kuliah yang diarsipkan tidak tampil pada daftar enrollment mahasiswa.
  - AC-03.4 Halaman detail mata kuliah menampilkan daftar materi, tugas, dan pengumuman.

### FR-04 — Pendaftaran mata kuliah (enrollment)
- **Aktor:** mahasiswa, admin · **Prioritas:** wajib
- **Deskripsi:** Mahasiswa mendaftar ke mata kuliah yang tersedia; admin dapat menambahkan
  atau menghapus peserta.
- **Alur utama:** mahasiswa membuka "Mata Kuliah" → memilih mata kuliah → "Daftar" →
  sistem mencatat enrollment → mata kuliah muncul di dasbor.
- **Alur alternatif:** sudah terdaftar → tombol berubah menjadi "Sudah terdaftar" dan
  permintaan kedua tidak membuat duplikat; kapasitas penuh (jika diaktifkan) → ditolak.
- **Kriteria penerimaan:**
  - AC-04.1 Satu mahasiswa tidak dapat memiliki dua enrollment pada mata kuliah yang sama.
  - AC-04.2 Setelah mendaftar, materi dan tugas mata kuliah tersebut dapat diakses.
  - AC-04.3 Pencarian mata kuliah tanpa hasil menampilkan keadaan kosong yang informatif
    ("Tidak ada mata kuliah yang cocok"), bukan halaman kosong atau error.

### FR-05 — Materi pembelajaran (Fitur Utama 1)
- **Aktor:** dosen (kelola), mahasiswa (lihat/unduh) · **Prioritas:** wajib
- **Deskripsi:** Dosen mengunggah materi berupa berkas atau tautan, dengan judul, pertemuan
  ke-berapa, deskripsi singkat, dan penanda wajib/tidak.
- **Alur utama:** dosen membuka mata kuliah → tab Materi → "Tambah materi" → mengisi judul
  dan pertemuan → memilih berkas atau menempel tautan → simpan → materi tampil di daftar
  dan dapat diunduh mahasiswa.
- **Alur alternatif:** berkas melebihi 5 MB → ditolak dengan pesan ukuran; ekstensi tidak
  diizinkan → ditolak dengan daftar format yang diterima; judul kosong → pesan validasi;
  dosen lain mencoba mengunggah ke mata kuliah bukan miliknya → 403.
- **Kriteria penerimaan:**
  - AC-05.1 Materi yang diunggah dapat diunduh mahasiswa terdaftar dan berkasnya identik
    (ukuran sama).
  - AC-05.2 Berkas 6 MB ditolak dan tidak tersimpan di penyimpanan.
  - AC-05.3 Berkas `.exe` ditolak.
  - AC-05.4 Mahasiswa yang tidak terdaftar mendapat 403 saat mengakses tautan materi.
  - AC-05.5 Daftar materi terurut berdasarkan pertemuan lalu judul.

### FR-06 — Pengelolaan tugas (Fitur Utama 2)
- **Aktor:** dosen · **Prioritas:** wajib
- **Deskripsi:** Dosen membuat tugas dengan judul, deskripsi, tenggat (tanggal + jam),
  nilai maksimum, dan lampiran opsional.
- **Alur utama:** dosen membuka tab Tugas → "Buat tugas" → mengisi data → simpan → tugas
  tampil dengan status "Aktif" atau "Lewat tenggat" berdasarkan waktu server.
- **Alur alternatif:** tenggat di masa lalu → ditolak; nilai maksimum ≤ 0 atau > 100 →
  ditolak; judul kosong → ditolak.
- **Kriteria penerimaan:**
  - AC-06.1 Tugas dengan tenggat kemarin tidak dapat disimpan.
  - AC-06.2 Status tugas berubah otomatis menjadi "Lewat tenggat" setelah waktu tenggat
    terlewati tanpa perlu tindakan manual.
  - AC-06.3 Tugas tampil pada dasbor mahasiswa peserta dengan hitung mundur tenggat.

### FR-07 — Pengumpulan tugas (Fitur Utama 2)
- **Aktor:** mahasiswa · **Prioritas:** wajib
- **Deskripsi:** Mahasiswa mengunggah satu berkas jawaban per tugas sebelum tenggat,
  dan dapat mengganti berkas selama belum dinilai.
- **Alur utama:** mahasiswa membuka tugas → "Kumpulkan" → memilih berkas → unggah →
  sistem memvalidasi format/ukuran/tenggat → menyimpan dengan stempel waktu server →
  menampilkan status "Terkumpul pada [waktu]".
- **Alur alternatif:** melewati tenggat → ditolak dengan pesan "Tenggat telah berakhir";
  format salah → ditolak; berkas kosong (0 byte) → ditolak; unggahan ulang setelah dinilai →
  ditolak dengan pesan "Tugas sudah dinilai".
- **Kriteria penerimaan:**
  - AC-07.1 Pengumpulan valid tersimpan dengan waktu server dan status "Terkumpul".
  - AC-07.2 Pengumpulan setelah tenggat ditolak; tidak ada record baru.
  - AC-07.3 Unggahan ulang sebelum tenggat dan sebelum dinilai menggantikan berkas lama
    (tetap satu record, versi lama tidak dihitung).
  - AC-07.4 Berkas > 5 MB dan ekstensi terlarang ditolak.
  - AC-07.5 Mahasiswa lain tidak dapat melihat berkas pengumpulan milik mahasiswa lain.

### FR-08 — Penilaian dan umpan balik (Fitur Utama 2)
- **Aktor:** dosen (menilai), mahasiswa (melihat) · **Prioritas:** wajib
- **Deskripsi:** Dosen melihat daftar pengumpulan satu tugas, membuka berkas, mengisi nilai
  dan umpan balik, lalu menyimpan. Mahasiswa melihat nilai dan umpan balik.
- **Alur utama:** dosen membuka tugas → tab Pengumpulan → memilih mahasiswa → mengisi nilai
  (0..nilai maksimum) dan umpan balik → simpan → status berubah "Dinilai" → mahasiswa
  melihat nilai pada halaman tugas dan dasbor.
- **Alur alternatif:** nilai di luar rentang → ditolak; nilai non-numerik → ditolak; menilai
  pengumpulan yang tidak ada → 404; dosen lain menilai tugas bukan miliknya → 403.
- **Kriteria penerimaan:**
  - AC-08.1 Nilai 101 pada tugas bernilai maksimum 100 ditolak.
  - AC-08.2 Setelah dinilai, mahasiswa melihat nilai dan umpan balik pada permintaan
    berikutnya.
  - AC-08.3 Rekap nilai menampilkan rata-rata dan jumlah yang sudah dinilai.

### FR-09 — Pengumuman mata kuliah
- **Aktor:** dosen · **Prioritas:** sebaiknya ada
- **Deskripsi:** Dosen menulis pengumuman (judul, isi) yang tampil di halaman mata kuliah
  dan dasbor mahasiswa, terurut dari yang terbaru.
- **Kriteria penerimaan:**
  - AC-09.1 Pengumuman baru tampil paling atas di halaman mata kuliah.
  - AC-09.2 Pengumuman hanya terlihat oleh peserta mata kuliah tersebut.
  - AC-09.3 Isi pengumuman yang mengandung tag HTML ditampilkan sebagai teks (tidak
    dieksekusi).

### FR-10 — Dasbor statistik
- **Aktor:** dosen, admin · **Prioritas:** sebaiknya ada (bahan video)
- **Deskripsi:** Menampilkan indikator agregat dari data nyata: jumlah peserta per mata
  kuliah, persentase pengumpulan per tugas, dan distribusi nilai (0–20, 21–40, …, 81–100).
- **Kriteria penerimaan:**
  - AC-10.1 Angka pada dasbor sama dengan hasil hitung manual pada data uji.
  - AC-10.2 Mata kuliah tanpa tugas menampilkan 0% atau keadaan kosong, bukan error
    pembagian nol.
  - AC-10.3 Grafik dirender dari data basis data, bukan angka statis di template.

---

## 4. Kebutuhan nonfungsional

| ID | Kategori | Kebutuhan | Cara mengukur |
|----|----------|-----------|---------------|
| NFR-01 | Kinerja | Halaman utama dan dasbor termuat < 3 detik pada koneksi 3G cepat; TTFB < 1 detik di lokal | DevTools Network, 3 kali pengukuran |
| NFR-02 | Keamanan | Kata sandi di-hash (PBKDF2/Argon2); CSRF aktif pada semua formulir POST; otorisasi dicek di server; berkas diunggah divalidasi ekstensi, MIME, dan ukuran; kredensial di `.env` | Pemeriksaan kode + TC-07 |
| NFR-03 | Keamanan sesi | Sesi berakhir setelah 60 menit tidak aktif; cookie `HttpOnly`, `SameSite=Lax` | Uji manual + `settings.py` |
| NFR-04 | Kegunaan | Pengguna baru dapat menyelesaikan pengumpulan tugas ≤ 3 menit tanpa pelatihan; setiap aksi memberi umpan balik | Uji coba 3 orang, catat waktu |
| NFR-05 | Kompatibilitas | Berfungsi pada Chrome, Edge, Firefox terbaru; tata letak tidak rusak pada 360 px, 768 px, 1366 px | Uji manual + tangkapan layar |
| NFR-06 | Keandalan data | Operasi multi-tabel (enrollment, penilaian) berjalan dalam transaksi; constraint unik pada surel, kode mata kuliah, pasangan (tugas, mahasiswa) | Uji + tinjauan model |
| NFR-07 | Keterpeliharaan | Pola MVT; nama model PascalCase, field snake_case, URL bahasa Indonesia; kode lolos `ruff check`; tidak ada fungsi > 50 baris tanpa alasan | Tinjauan kode |
| NFR-08 | Umpan balik kesalahan | Semua kesalahan 403/404/500 memakai halaman kustom berbahasa Indonesia dengan jalan kembali | Uji URL salah |
| NFR-09 | Aksesibilitas | Kontras teks ≥ 4.5:1; setiap input punya `<label>`; gambar punya `alt`; navigasi dapat dipakai dengan keyboard | Pemeriksaan manual |
| NFR-10 | Portabilitas | Konfigurasi melalui variabel lingkungan; dapat dijalankan di Linux dan Windows dengan langkah README yang sama | Uji di 2 mesin |

---

## 5. Kebutuhan data

### 5.1 Entitas utama

| Entitas | Deskripsi | Kunci unik |
|---------|-----------|------------|
| User | Akun dengan peran, NIM/NIDN, status aktif | surel |
| Course | Mata kuliah dengan dosen pengampu | kode |
| Enrollment | Relasi mahasiswa–mata kuliah | (course, student) |
| Material | Materi/berkas per pertemuan | — |
| Assignment | Tugas dengan tenggat dan nilai maksimum | — |
| Submission | Berkas jawaban mahasiswa per tugas | (assignment, student) |
| Announcement | Pengumuman per mata kuliah | — |

Kamus data lengkap, ERD, dan tipe field ada di
[04 — Rancangan Sistem §4](04-rancangan-sistem.md).

### 5.2 Aturan integritas data
1. Menghapus mata kuliah yang memiliki tugas **tidak** menghapus riwayat: gunakan arsip
   (`is_archived`), bukan `DELETE`.
2. Nilai tidak boleh melebihi `assignment.max_score`.
3. Stempel waktu pengumpulan berasal dari server (`timezone.now()`), bukan dari klien.
4. Berkas disimpan dengan nama acak; nama asli disimpan di kolom terpisah untuk ditampilkan.
5. Tidak ada data pribadi sensitif di luar nama, surel, dan NIM/NIDN.

### 5.3 Volume awal (untuk pengujian)
- 1 admin, 4 dosen, 30 mahasiswa, 6 mata kuliah, 24 materi, 12 tugas, ±200 pengumpulan.
  Data dibuat melalui perintah `python manage.py seed_demo`.

---

## 6. Batasan sistem (di luar ruang lingkup)

1. Tidak ada integrasi SIAKAD/API kampus; akun dikelola di dalam aplikasi.
2. Tidak ada pembayaran, presensi, atau penjadwalan ruang.
3. Tidak ada video conference atau streaming materi video besar.
4. Tidak ada aplikasi mobile native; antarmuka hanya web responsif.
5. Tidak ada obrolan real-time atau notifikasi surel/push.
6. Tidak ada multi-kampus, multi-bahasa, atau multi-tenant.
7. Berkas disimpan di sistem berkas lokal server, bukan object storage awan.
8. Tidak ada enkripsi data at-rest pada tingkat aplikasi (mengandalkan sistem operasi/DB).

Batasan ini **bukan** kekurangan implementasi, melainkan keputusan ruang lingkup yang
disepakati pada dokumen 01 §5.

## 7. Matriks keterlacakan ringkas

| FR | UC | TC | Dokumen rancangan |
|----|----|----|-------------------|
| FR-01 | UC-01 | TC-01, TC-07 | §3 diagram use case |
| FR-02 | UC-02 | — (uji manual) | §4 ERD |
| FR-03 | UC-03 | — | §4 ERD |
| FR-04 | UC-04 | TC-08 | §4 ERD |
| FR-05 | UC-05 | TC-02, TC-04, TC-07 | §5 flowchart, §6 wireframe |
| FR-06 | UC-06 | TC-03, TC-05 | §5 flowchart |
| FR-07 | UC-07 | TC-03, TC-04, TC-05 | §5 flowchart, §6 wireframe |
| FR-08 | UC-08 | TC-06 | §5 sequence |
| FR-09 | UC-09 | — | §4 ERD |
| FR-10 | UC-10 | — (bukti video) | §7 arsitektur |

Versi lengkap dengan kolom kode dan screenshot: [08 — Matriks Keterlacakan](08-matriks-keterlacakan.md).

---

**Riwayat revisi**

| Versi | Tanggal | Perubahan | Oleh |
|-------|---------|-----------|------|
| 0.1 | 22/11/2026 | Draf awal | Ridwan Rasyid |
| 1.0 | 24/11/2026 | ID kebutuhan dibekukan sebelum implementasi | Ridwan Rasyid |
