# 02 — Stakeholder, Peran, dan Hak Akses

## 1. Daftar stakeholder

| Kode | Stakeholder | Jenis | Kepentingan utama | Pengaruh |
|------|-------------|-------|-------------------|----------|
| ST-01 | Mahasiswa | Pengguna primer | Mengakses materi, mengumpulkan tugas, melihat nilai | Tinggi (pengguna harian) |
| ST-02 | Dosen | Pengguna primer | Mendistribusikan materi, mengelola tugas, menilai | Tinggi |
| ST-03 | Admin / operator program studi | Pengguna sekunder | Mengelola akun dan mata kuliah, memantau data | Sedang |
| ST-04 | Ketua program studi | Pengguna informasi | Melihat statistik perkuliahan untuk evaluasi | Sedang |
| ST-05 | Tim pengembang (kelompok) | Produsen | Membangun, menguji, mendokumentasikan | Tinggi |

> **TODO:** wawancara singkat (5–10 menit) dengan 1 mahasiswa dan 1 dosen, lalu tambahkan
> 1–2 kutipan kebutuhan nyata di sini. Satu paragraf bukti wawancara menaikkan kredibilitas
> bagian analisis kebutuhan secara signifikan.

## 2. Profil pengguna

| Peran | Tingkat teknis | Konteks pemakaian | Kebutuhan utama |
|-------|----------------|-------------------|-----------------|
| Mahasiswa | Menengah; terbiasa aplikasi web dan ponsel | Kampus, jaringan tidak stabil, sering dari ponsel | Navigasi sederhana, tenggat jelas, unggah berkas cepat, umpan balik error yang spesifik |
| Dosen | Menengah–tinggi | Ruang dosen, desktop | Daftar pengumpulan rapi, penilaian cepat, unggah banyak materi |
| Admin | Tinggi | Desktop | CRUD massal, pencarian, konsistensi data |
| Ketua prodi | Menengah | Desktop, sesekali | Ringkasan angka, ekspor/laporan |

## 3. Matriks hak akses (actor × aktivitas)

Legenda: **✓** penuh · **○** terbatas pada data miliknya · **—** tidak boleh.
`RBAC` di SRS (FR-01) mengimplementasikan tabel ini secara harfiah.

| Aktivitas | Tamu | Mahasiswa | Dosen | Admin |
|-----------|:----:|:---------:|:-----:|:-----:|
| Melihat halaman beranda publik | ✓ | ✓ | ✓ | ✓ |
| Login / logout | ✓ | ✓ | ✓ | ✓ |
| Melihat daftar mata kuliah | — | ○ (yang diikuti) | ○ (yang diampu) | ✓ |
| Mendaftar mata kuliah (enrollment) | — | ○ | — | ✓ |
| Melihat materi | — | ○ | ○ | ✓ |
| Mengunggah / menghapus materi | — | — | ○ | ✓ |
| Membuat / mengubah tugas | — | — | ○ | ✓ |
| Mengumpulkan tugas | — | ○ | — | — |
| Melihat daftar pengumpulan | — | ○ (miliknya) | ○ (tugasnya) | ✓ |
| Menilai dan memberi umpan balik | — | — | ○ | — |
| Melihat nilai | — | ○ | ○ | ✓ |
| Menulis pengumuman | — | — | ○ | ✓ |
| Mengelola pengguna (buat, ubah, nonaktifkan) | — | — | — | ✓ |
| Mengelola mata kuliah (buat, ubah, arsip) | — | — | — | ✓ |
| Melihat dasbor statistik | — | ○ (ringkasan pribadi) | ○ (mata kuliahnya) | ✓ |

## 4. Kebutuhan per stakeholder

### ST-01 Mahasiswa
- Melihat semua mata kuliah yang diikuti dalam satu daftar, dengan tenggat terdekat di atas.
- Mengunduh materi tanpa harus login ulang di tengah sesi.
- Mengunggah tugas dan langsung melihat konfirmasi "berhasil" atau alasan penolakan.
- Melihat status: belum mengumpulkan / sudah mengumpulkan / sudah dinilai.
- Melihat nilai dan umpan balik setelah dosen menilai.

### ST-02 Dosen
- Membuat tugas dengan tenggat dan nilai maksimum; sistem menolak tenggat di masa lalu.
- Melihat satu tabel pengumpulan: nama, waktu unggah, berkas, status, nilai.
- Memberi nilai dan umpan balik tanpa berpindah halaman berulang kali.
- Mengunggah materi per pertemuan dan menandai materi mana yang wajib.

### ST-03 Admin
- Membuat akun massal (minimal satu per satu dengan formulir yang jelas).
- Menonaktifkan akun tanpa menghapus riwayat nilainya.
- Mengelola mata kuliah dan menetapkan dosen pengampu.

### ST-04 Ketua program studi
- Melihat statistik: jumlah peserta per mata kuliah, tingkat pengumpulan, sebaran nilai.
- Mengetahui keterbatasan data (hanya data aplikasi, bukan data akademik resmi).

## 5. Batasan akses yang wajib diuji

Aturan berikut menjadi dasar test case otorisasi (TC-07):

1. Mahasiswa tidak dapat membuka mata kuliah yang tidak diikutinya, termasuk dengan
   menebak ID pada URL.
2. Dosen tidak dapat mengubah tugas atau menilai mata kuliah milik dosen lain.
3. Mahasiswa tidak dapat membuka halaman penilaian meskipun mengetahui URL-nya.
4. Pengguna yang belum login diarahkan ke halaman login, bukan ke halaman error 500.
5. Akun nonaktif tidak dapat login dan sesi aktifnya diakhiri pada permintaan berikutnya.

> **TODO:** pastikan setiap baris di bagian 5 punya test case atau minimal catatan
> pengujian manual. Inilah bukti nyata "hak akses sesuai konteks".
