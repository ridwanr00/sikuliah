# 10 — Panduan Screenshot dan Video Presentasi

Brief meminta minimal 4 screenshot dan video ≥ 3 menit yang memperlihatkan aplikasi berjalan,
fitur utama, **dua temuan berbasis statistik/grafik**, dan **satu keterbatasan** data atau
analisis. Dokumen ini adalah daftar bidik dan naskah agar tidak ada yang terlewat.

---

## 1. Screenshot wajib

Simpan di `screenshots/` dengan nama yang sudah ditentukan, agar bisa langsung dirujuk dari
PDF dan matriks keterlacakan.

| No | Berkas | Isi yang harus terlihat | Wajib? |
|----|--------|-------------------------|--------|
| 1 | `01-beranda.png` | Halaman utama + identitas aplikasi + navigasi | ✅ |
| 2 | `02-materi-dosen.png` | Fitur Utama 1: daftar materi yang dikelola dosen | ✅ |
| 3 | `03-materi-mahasiswa.png` | Mahasiswa mengunduh materi | ✅ |
| 4 | `04-submit-tugas.png` | Fitur Utama 2: form pengumpulan + status berhasil | ✅ |
| 5 | `05-daftar-pengumpulan.png` | Tabel pengumpulan dosen (nama, waktu, berkas, nilai) | ✅ |
| 6 | `06-nilai-mahasiswa.png` | Nilai + umpan balik tampil di akun mahasiswa | ✅ |
| 7 | `07-statistik.png` | Dasbor statistik dengan grafik | ✅ (bahan video) |
| 8 | `08-validasi-error.png` | Pesan validasi berkas (ukuran/ekstensi) | disarankan |
| 9 | `09-403.png` | Halaman 403 saat akses lintas peran | disarankan |
| 10 | `10-responsif-360px.png` | Tampilan ponsel | disarankan |

### Aturan pengambilan
- **Dari aplikasi yang benar-benar berjalan** (bukan Figma/mockup). Tampilkan URL atau
  bilah peramban pada minimal satu gambar.
- Resolusi seragam: jendela 1366×768 atau 1440×900; zoom 100%.
- Data harus masuk akal dan konsisten antar screenshot (nama mahasiswa sama, tugas sama).
- Jangan menampilkan data pribadi nyata, token, atau kata sandi.
- Simpan juga versi PNG tanpa kompresi berlebih; jangan crop sampai konteks hilang
  (navbar dan judul halaman sebaiknya tetap terlihat).

---

## 2. Naskah video (target 3 menit 30 detik)

| Waktu | Bagian | Isi | Visual |
|-------|--------|-----|--------|
| 0:00–0:20 | Pembuka | Nama kelompok, anggota, judul, masalah yang diselesaikan (1 kalimat) | Slide judul / beranda |
| 0:20–0:40 | Konteks | Tiga peran, dua fitur utama, teknologi (Python/Django) | Diagram arsitektur (Gambar 4.1/§1) |
| 0:40–1:30 | Demo Fitur Utama 1 | Login dosen → unggah materi → login mahasiswa → unduh; tunjukkan validasi berkas gagal | Rekaman layar |
| 1:30–2:30 | Demo Fitur Utama 2 | Buat tugas → mahasiswa kumpulkan → dosen nilai → mahasiswa lihat nilai; tunjukkan penolakan lewat tenggat | Rekaman layar |
| 2:30–3:05 | Statistik | Dasbor: **temuan 1**, **temuan 2**, **keterbatasan** | Grafik + angka |
| 3:05–3:25 | Penutup | Kesimpulan, keterbatasan, saran pengembangan | Slide penutup |

### Naskah bagian statistik (wajib diisi angka nyata)

> "Dari data demo 2 mata kuliah, 60 mahasiswa, dan 8 tugas, dasbor menunjukkan dua temuan.
> **Pertama**, tingkat pengumpulan tugas turun dari 92% pada tugas pertama menjadi 61% pada
> tugas keempat — penurunan terbesar terjadi setelah tenggat berdekatan dengan ujian.
> **Kedua**, rata-rata nilai tugas berkelompok (82,4) lebih tinggi daripada tugas individu
> (74,1), selisih 8,3 poin.
> Keterbatasan analisis ini: data berasal dari 60 akun demo dalam satu program studi dan
> hanya mencakup satu semester, sehingga tidak dapat digeneralisasi; sistem juga belum
> mencatat alasan mahasiswa tidak mengumpulkan."

> **TODO:** ganti angka di atas dengan hasil nyata dari dasbor kalian. Hitung ulang secara
> manual minimal sekali agar bisa menjawab bila ditanya "angka ini dari mana?".

---

## 3. Produksi video

| Aspek | Ketentuan |
|-------|-----------|
| Durasi | ≥ 3 menit (target 3:30 agar ada margin) |
| Resolusi | 1920×1080, 30 fps |
| Alat | OBS Studio (Scene: layar penuh + webcam opsional) |
| Audio | Narasi jelas; rekam terpisah lalu sinkronkan bila perlu; hindari musik keras |
| Kursor | Tampilkan klik (OBS: "Show mouse cursor" + highlight) |
| Perbesaran | Zoom 110–125% pada editor agar teks terbaca di video |
| Berkas | `.mp4` (H.264) bila diunggah; bila tautan, pastikan dapat diakses publik |
| Judul berkas | `Video Presentasi_Kelompok 22.mp4` |

### Checklist sebelum merekam
- [ ] Data demo sudah di-seed dan konsisten.
- [ ] Tugas dengan tenggat lewat tersedia untuk didemokan.
- [ ] Semua tab lain ditutup; notifikasi dinonaktifkan.
- [ ] Tidak ada kata sandi terlihat di layar (isi form perlahan atau siapkan akun demo).
- [ ] Latihan sekali tanpa rekaman untuk mengukur waktu.
- [ ] Rekaman cadangan disimpan sebelum presentasi (mitigasi R-06).

---

## 4. Struktur slide pendukung (opsional, 4 slide)

1. **Judul** — nama aplikasi, kelompok, anggota.
2. **Masalah → solusi** — 3 poin masalah, 3 poin solusi.
3. **Arsitektur & teknologi** — Gambar arsitektur + alasan singkat Python/Django.
4. **Statistik** — dua grafik + dua temuan + satu keterbatasan.

Untuk PDF, urutan gambar yang disarankan: beranda → alur dosen → alur mahasiswa → statistik
→ bukti validasi/error → tampilan responsif.
