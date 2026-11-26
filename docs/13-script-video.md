# 13 — Naskah Video Presentasi

**Durasi target:** 3 menit 40 detik (batas minimal brief: 3 menit)
**Resolusi:** 1920×1080, 30 fps · **Berkas:** `Video Presentasi_Kelompok 22.mp4`
**Narator:** Ridwan Rasyid (dikerjakan mandiri)

Naskah ini memakai **angka nyata** dari data demo. Angka dapat berubah bila data di-seed
ulang — baca ulang dari layar saat merekam dan sesuaikan kalimat yang ditandai `[...]`.

---

## 1. Persiapan sebelum merekam (15 menit)

### 1.1 Nyalakan aplikasi

```bash
cd src
../.venv/bin/python manage.py runserver
```

Buka <http://127.0.0.1:8000> di Chrome/Brave.

### 1.2 Siapkan berkas contoh

```bash
mkdir -p ~/demo
cp src/media/materials/2026/11/*.pdf ~/demo/materi-uji.pdf
cp src/media/materials/2026/11/*.pdf ~/demo/jawaban-demo.pdf
printf 'bukan berkas yang diizinkan' > ~/demo/contoh.exe
```

### 1.3 Pastikan akun demo masih "bersih"

Akun `demo@kampus.test` sengaja tidak punya pengumpulan, supaya alur kumpulkan → nilai →
lihat nilai selalu bisa diperagakan. Reset bila sudah terpakai:

```bash
cd src
../.venv/bin/python manage.py shell -c \
  "from apps.assignments.models import Submission; \
   Submission.objects.filter(student__email='demo@kampus.test').delete(); print('bersih')"
```

Kredensial ada di `CREDENTIALS.local.md` (tidak di-commit). Jangan menampilkan berkas itu,
`.env`, atau dashboard Neon/Backblaze saat merekam.

### 1.4 Setelan layar

- [ ] Tutup tab lain, matikan notifikasi, sembunyikan bookmark bar.
- [ ] Zoom peramban **110%** agar teks terbaca.
- [ ] Kursor terlihat (OBS: *Show mouse cursor*).
- [ ] Bilah alamat terlihat pada minimal satu adegan (bukti aplikasi berjalan).
- [ ] Siapkan 3 tab: **aplikasi**, **dasbor dosen**, **bucket B2** (opsional).

### 1.5 Data yang akan disebut

| Angka | Nilai sekarang | Di mana melihat |
|-------|----------------|-----------------|
| Mata kuliah dosen1 | 2 (IF-301, IF-305) | Dasbor dosen |
| Peserta terdaftar | 42 | Kartu dasbor |
| Tingkat pengumpulan | 87% (73/84) | Kartu dasbor |
| Rata-rata nilai | 79,3 (58 dinilai) | Kartu dasbor |
| Sebaran nilai | 26 di 61–80; 32 di 81–100 | Grafik dasbor |
| IF-301 Tugas 1 | 29/30 terkumpul (97%) | Daftar pengumpulan |
| IF-301 Tugas 2 | 23/30 terkumpul (77%) | Daftar pengumpulan |

---

## 2. Naskah per segmen

### Segmen 1 — Pembuka (0:00–0:22)

**Visual:** halaman beranda SIKULIAH, kursor diam.

> "Selamat pagi. Saya Ridwan Rasyid, NIM 1003260037, dari Kelompok 22.
> Video ini mendemonstrasikan **SIKULIAH**, aplikasi *learning management system* yang
> saya bangun dengan Python dan Django untuk mata kuliah Rekayasa Perangkat Lunak.
> Aplikasi ini punya tiga peran: admin, dosen, dan mahasiswa."

**Teks layar:** `SIKULIAH — LMS Kampus · Kelompok 22`

---

### Segmen 2 — Masalah dan solusi (0:22–0:45)

**Visual:** tetap di beranda; scroll perlahan ke bagian "Tiga peran, tiga tampilan".

> "Latar belakangnya: materi kuliah sering tersebar di grup chat, tugas dikumpulkan lewat
> surel, dan nilai direkap manual. Dosen sulit melacak siapa yang sudah mengumpulkan,
> sementara mahasiswa tidak tahu status penilaiannya.
> SIKULIAH memusatkan materi, tugas, penilaian, dan statistik dalam satu tempat.
> Dua fitur utamanya adalah **pengelolaan materi** dan **pengumpulan serta penilaian tugas**."

---

### Segmen 3 — Fitur utama 1: materi (0:45–1:40)

**Visual (dosen):**
1. Klik **Masuk** → login `dosen1@kampus.test`.
2. Tunjukkan sebentar dasbor (jangan jelaskan angka dulu).
3. **Mata Kuliah** → **IF-301 Rekayasa Perangkat Lunak**.
4. Klik **+ Materi** → isi judul `Materi Uji Video`, pertemuan `7`, unggah
   `~/demo/materi-uji.pdf` → **Unggah materi**.
5. Materi baru tampil di daftar, lalu klik **Unduh** sekali untuk membuktikan berkas utuh.
6. Ulangi **+ Materi** dengan `contoh.exe` → tunjukkan pesan
   *"Format .exe tidak diizinkan…"* → **Batal**.

> "Saya masuk sebagai dosen. Di halaman mata kuliah ada tiga bagian: materi, tugas, dan
> pengumuman. Saya tambahkan materi untuk pertemuan tujuh, memilih berkas PDF, lalu
> menyimpan. Materi langsung muncul di daftar dan bisa diunduh.
> Sistem juga memvalidasi berkas. Saya coba unggah berkas berekstensi **exe**, dan aplikasi
> menolaknya dengan pesan yang jelas: format harus PDF, DOCX, PPTX, atau ZIP, maksimal lima
> megabita. Validasi ini diperiksa di server, bukan hanya di tampilan."

**Visual (mahasiswa):** keluar → login `demo@kampus.test` → **Mata Kuliah** → **IF-301** →
bagian Materi → klik **Unduh**.

> "Sekarang saya masuk sebagai mahasiswa. Materi yang sama terlihat di mata kuliah yang
> saya ikuti, dan dapat diunduh. Mahasiswa yang tidak terdaftar tidak bisa membuka halaman
> ini — sistem mengembalikan pesan **403**, bukan halaman kosong."

---

### Segmen 4 — Fitur utama 2: tugas dan penilaian (1:40–2:45)

**Visual (mahasiswa):** masih sebagai `demo@kampus.test`.
1. Buka **Tugas 2 — Perancangan Sistem**.
2. Tunjukkan tenggat dan nilai maksimum.
3. Pilih `~/demo/jawaban-demo.pdf` → **Kumpulkan**.
4. Status berubah menjadi **Terkumpul** dengan waktu server.
5. Buka **Tugas 1** (sudah lewat tenggat) → tunjukkan label **Lewat tenggat** dan tidak ada
   formulir pengumpulan.

> "Sebagai mahasiswa, saya membuka Tugas 2. Terlihat tenggat dan nilai maksimumnya.
> Saya unggah berkas jawaban, lalu sistem mencatat waktu pengumpulan dari server.
> Kalau saya membuka tugas yang tenggatnya sudah lewat, formulir pengumpulan tidak muncul
> dan sistem menolak pengumpulan, walaupun URL-nya diketik langsung."

**Visual (dosen):** keluar → login `dosen1` → **IF-301** → bagian Tugas →
**Pengumpulan** pada Tugas 2.
1. Cari `Demo` pada kolom pencarian.
2. Klik **Nilai** pada baris **Mahasiswa Demo**.
3. Isi nilai `90`, umpan balik: `Struktur jawaban baik. Pertajam bagian analisis risiko.`
4. **Simpan nilai** → baris menampilkan badge `90`.

> "Sebagai dosen, saya membuka daftar pengumpulan. Ada rekap peserta, jumlah terkumpul,
> yang sudah dinilai, dan rata-rata. Saya cari mahasiswa demo, membuka berkasnya, lalu
> memberi nilai sembilan puluh dan umpan balik. Nilai di luar rentang nol sampai seratus
> akan ditolak oleh validasi."

**Visual (mahasiswa):** login `demo@kampus.test` → buka **Tugas 2**.
Tunjukkan kartu **Nilai dan umpan balik** berisi `90/100`.

> "Kembali sebagai mahasiswa, nilai dan umpan balik langsung terlihat. Tidak perlu menunggu
> pengumuman manual, dan berkas tidak bisa diganti setelah dinilai."

---

### Segmen 5 — Statistik: dua temuan dan satu keterbatasan (2:45–3:20)

**Visual:** login `dosen1` → **Dasbor**. Sorot kartu angka, lalu grafik **Sebaran nilai**.
Buka **IF-301 → Tugas → Pengumpulan** untuk temuan pertama (bila perlu).

> "Dasbor menampilkan ringkasan dari data nyata. Dari dua mata kuliah, empat puluh satu
> peserta, tingkat pengumpulan **delapan puluh tujuh persen**, yaitu tujuh puluh tiga
> dari delapan puluh empat pengumpulan, dengan rata-rata nilai **tujuh puluh sembilan koma
> tiga**.
>
> **Temuan pertama:** tingkat pengumpulan turun dari **sembilan puluh tujuh persen** pada
> Tugas 1 menjadi **tujuh puluh tujuh persen** pada Tugas 2 di IF-301. Artinya tujuh dari
> tiga puluh mahasiswa belum mengumpulkan tugas kedua.
>
> **Temuan kedua:** seluruh lima puluh delapan nilai yang sudah masuk berada di rentang
> **enam puluh satu sampai seratus** — dua puluh enam di rentang enam puluh satu sampai
> delapan puluh, dan tiga puluh dua di rentang delapan puluh satu sampai seratus. Tidak ada
> nilai di bawah enam puluh.
>
> **Keterbatasan:** data ini berasal dari tiga puluh enam akun demo dalam satu program studi
> dan satu semester, jadi tidak bisa digeneralisasi. Sistem juga belum mencatat alasan
> mahasiswa tidak mengumpulkan, sehingga penurunan pada temuan pertama belum bisa
> dijelaskan secara kausal."

> **Bila angka di layar berbeda:** sebut angka yang terlihat, lalu sesuaikan kalimat
> "turun dari X persen menjadi Y persen". Rumus: `terkumpul ÷ peserta × 100`.

---

### Segmen 6 — Penutup (3:20–3:40)

**Visual:** kembali ke dasbor atau beranda; kursor diam.

> "Kesimpulannya, SIKULIAH sudah menjalankan dua fitur utama: distribusi materi dengan
> validasi berkas, serta pengumpulan dan penilaian tugas dengan aturan tenggat dan hak
> akses. Keterbatasannya adalah data masih berupa data demo dan berkas pada paket gratis
> bersifat sementara. Saran pengembangan: integrasi SIAKAD, notifikasi surel, dan
> penyimpanan permanen.
> Terima kasih."

---

## 3. Versi padat (3 menit 5 detik)

Bila ingin lebih pendek, potong dengan urutan ini:

| Dipotong | Hemat |
|----------|-------|
| Segmen 2 dipersingkat jadi 1 kalimat masalah | 10 detik |
| Demo unggah materi hanya satu kali (tanpa percobaan `.exe`) | 15 detik |
| Penjelasan 403 di segmen 3 dihapus | 8 detik |
| Temuan kedua cukup satu kalimat | 10 detik |

Jangan memotong: demonstrasi pengumpulan, penilaian, dan bagian statistik (tiga hal yang
secara eksplisit diminta brief).

---

## 4. Tips teknis saat merekam

1. Rekam **per segmen**, bukan sekali jadi; gabungkan di editor. Lebih cepat mengulang.
2. Bicara sedikit lebih lambat daripada percakapan biasa; beri jeda satu detik setelah
   angka penting.
3. Gerakkan kursor ke elemen yang sedang dibahas, lalu diam — jangan menggoyang kursor.
4. Hindari kata "semuanya sempurna" atau "tanpa bug". Sebut keterbatasan secara terbuka.
5. Jangan memperlihatkan: `CREDENTIALS.local.md`, `src/.env`, dashboard Neon, dashboard
   Backblaze, atau kata sandi yang diketik.
6. Rekam cadangan (file kedua) sebelum presentasi.

## 5. Antisipasi pertanyaan penguji

| Pertanyaan | Jawaban singkat |
|------------|-----------------|
| Kenapa Django, bukan Flask? | Autentikasi, form, validasi, migrasi, dan panel admin sudah tersedia; waktu habis untuk fitur, bukan infrastruktur. |
| Bagaimana mencegah mahasiswa mengumpulkan terlambat? | Dicek di server memakai `timezone.now()` pada setiap POST, bukan hanya menonaktifkan tombol. |
| Bagaimana mencegah mahasiswa melihat berkas lain? | Setiap unduhan memeriksa pemilik atau dosen pengampu; pelanggaran menghasilkan 403. |
| Di mana data disimpan? | Produksi: Neon Postgres; berkas di object storage Backblaze B2. Lokal: SQLite dan folder `media/`. |
| Apa keterbatasan terbesar? | Data demo, satu prodi, tanpa integrasi SIAKAD; berkas pada paket gratis perlu object storage agar permanen. |
| Apakah pengujian dilakukan pada aplikasi nyata? | Ya — 15 test otomatis lulus, 8 test case manual, dan 10 screenshot dari aplikasi berjalan. |

## 6. Checklist setelah merekam

- [ ] Durasi ≥ 3 menit.
- [ ] Dua temuan statistik disebut dengan angka.
- [ ] Satu keterbatasan disebut eksplisit.
- [ ] Kedua fitur utama terlihat berfungsi.
- [ ] Tidak ada kredensial/rahasia di layar.
- [ ] Audio jelas, teks terbaca pada 1080p.
- [ ] Berkas dinamai `Video Presentasi_Kelompok 22.mp4`.
