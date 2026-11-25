# 01 — Latar Belakang, Tujuan, dan Ruang Lingkup

## 1. Latar belakang masalah

Kegiatan perkuliahan di program studi masih banyak dikelola melalui kanal yang terpisah:
materi dibagikan lewat grup pesan instan, pengumpulan tugas melalui surel atau tautan
penyimpanan awan, nilai direkap manual di lembar kerja, dan pengumuman tersebar di
beberapa tempat. Kondisi ini menimbulkan beberapa masalah nyata:

1. **Materi tidak terpusat.** Mahasiswa harus mencari file di riwayat percakapan; file
   yang sama tersimpan dalam beberapa versi tanpa penanda mana yang berlaku.
2. **Pengumpulan tugas sulit dilacak.** Dosen tidak punya daftar tunggal siapa yang sudah
   mengumpulkan, kapan dikumpulkan, dan file mana yang terakhir. Tugas yang masuk setelah
   tenggat sering tidak terdeteksi.
3. **Penilaian dan umpan balik lambat serta tidak transparan.** Mahasiswa tidak dapat
   melihat status penilaian tanpa bertanya langsung kepada dosen.
4. **Rekap perkuliahan tidak tersedia.** Tidak ada data agregat seperti tingkat
   pengumpulan tugas atau sebaran nilai yang bisa dipakai untuk evaluasi tengah semester.
5. **Berkas mudah hilang atau tertukar.** Penamaan file yang tidak konsisten dan tidak ada
   pencatatan waktu unggah menyulitkan audit sederhana.

Learning management system (LMS) ringan yang khusus melayani kebutuhan tersebut dinilai
cukup untuk menyelesaikan masalah tanpa harus mengadopsi platform besar yang kompleks dan
berbayar.

## 2. Rumusan masalah

1. Bagaimana memusatkan distribusi materi dan tugas dalam satu sistem yang mudah diakses
   dosen dan mahasiswa?
2. Bagaimana memastikan pengumpulan tugas tercatat lengkap dengan waktu unggah dan
   validasi berkas, termasuk penolakan pengumpulan setelah tenggat?
3. Bagaimana menyajikan nilai dan umpan balik kepada mahasiswa secara langsung?
4. Bagaimana menyediakan data agregat perkuliahan sebagai dasar evaluasi?

## 3. Tujuan

| Kode | Tujuan | Indikator keberhasilan |
|------|--------|------------------------|
| T-01 | Menyediakan satu tempat untuk materi, tugas, dan pengumuman per mata kuliah | Seluruh materi satu mata kuliah dapat diakses dari satu halaman mata kuliah |
| T-02 | Mencatat pengumpulan tugas secara otomatis dan valid | Setiap pengumpulan tersimpan dengan waktu, berkas, dan status; berkas tidak valid ditolak |
| T-03 | Mempercepat pemberian nilai dan umpan balik | Dosen dapat menilai dari satu daftar tanpa membuka berkas di luar aplikasi |
| T-04 | Memberi transparansi nilai kepada mahasiswa | Mahasiswa melihat nilai dan umpan balik tanpa menunggu pengumuman manual |
| T-05 | Menyediakan statistik perkuliahan | Dasbor menampilkan minimal 3 indikator agregat dari data nyata |

## 4. Manfaat

| Pihak | Manfaat |
|-------|---------|
| Mahasiswa | Materi dan tenggat terpusat; status pengumpulan dan nilai terlihat jelas; tidak perlu menanyakan hal administratif |
| Dosen | Rekap pengumpulan otomatis; penilaian terpusat; pengumuman sekali tulis |
| Admin / program studi | Data pengguna dan mata kuliah terkendali; statistik untuk evaluasi |
| Program studi | Jejak digital perkuliahan yang dapat diaudit |

## 5. Ruang lingkup

**Termasuk:**

- Autentikasi dan otorisasi tiga peran (admin, dosen, mahasiswa).
- Pengelolaan pengguna, mata kuliah, dan pendaftaran mata kuliah.
- Unggah dan unduh materi pembelajaran per pertemuan.
- Pembuatan tugas dengan tenggat, pengumpulan berkas, penilaian, dan umpan balik.
- Pengumuman per mata kuliah.
- Dasbor statistik: jumlah peserta, tingkat pengumpulan, distribusi nilai.

**Tidak termasuk (lihat juga SRS bab 6):**

- Integrasi SIAKAD, pembayaran, presensi biometrik, video conference.
- Aplikasi mobile native, notifikasi push, obrolan real-time.
- Pembelajaran adaptif, kuis otomatis, atau analitik prediktif.
- Multi-kampus, multi-bahasa, dan penyimpanan objek awan produksi.

## 6. Definisi istilah

| Istilah | Arti dalam dokumen ini |
|---------|------------------------|
| LMS | Learning Management System — sistem pengelolaan pembelajaran daring |
| Mata kuliah | Unit pembelajaran dengan kode, nama, SKS, dan satu dosen pengampu (dalam proyek ini) |
| Materi | Berkas atau tautan pembelajaran yang diunggah dosen untuk pertemuan tertentu |
| Tugas | Aktivitas penilaian dengan deskripsi, tenggat, dan nilai maksimum |
| Pengumpulan | Rekaman berkas yang diunggah mahasiswa untuk satu tugas |
| Enrollment | Pendaftaran mahasiswa pada sebuah mata kuliah |
| RBAC | Role-Based Access Control — pembatasan akses berdasarkan peran |
| Tenggat | Batas waktu pengumpulan tugas |

> **TODO:** tambahkan minimal 2 rujukan nyata pada bagian ini bila dosen meminta sitasi
> (mis. buku Sommerville, *Software Engineering*, atau IEEE 830 untuk format SRS), lalu
> cantumkan di SRS bagian 1.4 Referensi.
