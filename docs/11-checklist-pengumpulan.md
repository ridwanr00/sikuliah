# 11 — Checklist Pengumpulan

Gunakan daftar ini H-1 sebelum deadline. Setiap kotak harus tercentang; jangan menilai
sendiri "sudah cukup".

---

## 1. Kelengkapan berkas (sesuai brief slide 11–13)

### 1.1 Dokumentasi PDF
- [ ] Berkas `Dokumentasi Proyek_Kelompok 22.pdf` ada dan dapat dibuka.
- [ ] Memuat **identitas kelompok** (nama, NIM, peran) dan judul.
- [ ] Memuat deskripsi & tujuan website.
- [ ] Memuat latar belakang permasalahan.
- [ ] Memuat stakeholder (peran, kebutuhan, hak akses).
- [ ] Memuat model pengembangan + alasan + penerapan tahapan.
- [ ] Memuat SRS lengkap (deskripsi sistem, ruang lingkup, pengguna, FR, NFR, data,
      batasan, kriteria penerimaan).
- [ ] Memuat seluruh diagram: use case, flowchart, ERD, arsitektur, alur interaksi,
      wireframe.
- [ ] Memuat teknologi + alasan pemilihan.
- [ ] Memuat struktur source code.
- [ ] Memuat pengelolaan data (kamus data/ERD).
- [ ] Memuat implementasi fitur (dengan rujukan FR).
- [ ] Memuat risiko + dampak + mitigasi (≥ 3).
- [ ] Memuat hasil pengujian (≥ 5 TC, hasil aktual, status).
- [ ] Memuat screenshot implementasi.
- [ ] Memuat keterbatasan sistem.
- [ ] Memuat kesimpulan dan saran pengembangan.
- [ ] Ada daftar isi, nomor halaman, dan penomoran gambar/tabel.

### 1.2 File pendukung
- [ ] `README.md` memuat: identitas & deskripsi, fitur utama, teknologi, struktur folder,
      persyaratan, instalasi, konfigurasi, cara menjalankan, cara menggunakan,
      penanganan masalah umum.
- [ ] `requirements.txt` lengkap dan dapat dipasang dari nol.
- [ ] `.env.example` tersedia; **tidak ada** `.env` asli.
- [ ] Source code lengkap, tanpa `vendor/`, `node_modules/`, `.venv/`, `media/` berisi data
      pribadi.
- [ ] Data pendukung: seeder/SQL dump agar aplikasi tidak kosong saat dijalankan.
- [ ] Tidak ada kredensial, token, atau kunci API di repositori/PDF.

### 1.3 Screenshot
- [ ] Halaman utama.
- [ ] Fitur utama pertama.
- [ ] Fitur utama kedua.
- [ ] Hasil interaksi pengguna (submit, nilai, statistik).
- [ ] Berasal dari aplikasi yang benar-benar dijalankan.
- [ ] Nama berkas sesuai dokumen 10.

### 1.4 Video
- [ ] Durasi ≥ 3 menit.
- [ ] Memperlihatkan aplikasi berjalan.
- [ ] Menjelaskan fitur utama.
- [ ] Menampilkan minimal **2 temuan** berbasis statistik/grafik.
- [ ] Menyebut minimal **1 keterbatasan** dataset/analisis.
- [ ] Audio jelas, teks terbaca (1080p).

### 1.5 Pengemasan
- [ ] Satu file ZIP dengan nama:
      `Tugas 1 Kelompok_Rekayasa Perangkat Lunak_Kelompok 22.zip`
- [ ] Struktur di dalam ZIP rapi (satu folder utama, bukan file berserakan).
- [ ] Ukuran wajar; video besar memakai tautan yang dapat diakses.

---

## 2. Uji "mesin bersih" (wajib)

Ekstrak ZIP ke folder baru (atau komputer anggota lain) dan ikuti README **tanpa
penjelasan tambahan**. Catat setiap langkah yang gagal.

```bash
unzip "Tugas 1 Kelompok_Rekayasa Perangkat Lunak_Kelompok 22.zip"
cd [folder-hasil-ekstrak]
python -m venv .venv && source .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env        # isi SECRET_KEY
python manage.py migrate
python manage.py seed_demo
python manage.py runserver
```

| Pemeriksaan | Lulus? |
|-------------|:------:|
| Instalasi selesai tanpa error | ⬜ |
| Migrasi berjalan tanpa error | ⬜ |
| Data demo muncul | ⬜ |
| Login 3 peran berhasil | ⬜ |
| Fitur utama 1 dapat didemokan | ⬜ |
| Fitur utama 2 dapat didemokan | ⬜ |

> **TODO:** minta anggota yang **tidak** menulis README untuk melakukan uji ini. Penulis
> README selalu tidak sadar langkah yang ia lewati.

---

## 3. Konsistensi dokumen vs aplikasi

| Periksa | Cara | Hasil |
|---------|------|-------|
| Semua FR di SRS ada di aplikasi | Buka dokumen 08 §1 | ⬜ |
| Semua menu di aplikasi ada di SRS | Audit `urls.py` (dok. 08 §3) | ⬜ |
| Nama fitur konsisten (SRS, PDF, video) | Cari istilah berbeda | ⬜ |
| Screenshot sesuai UI terbaru | Bandingkan dengan aplikasi | ⬜ |
| Angka statistik di video = angka aplikasi | Hitung ulang | ⬜ |
| Hasil TC = perilaku aplikasi saat ini | Ulangi 2 TC acak | ⬜ |

---

## 4. Kesalahan yang paling sering menghilangkan nilai

1. **Fitur di PDF tidak ada di aplikasi** (atau sebaliknya). → audit dokumen 08.
2. **Pengujian hanya jalur bahagia.** Brief meminta kondisi kesalahan; TC-04/05/07 sudah
   menutup ini — jangan dihapus.
3. **Hasil aktual TC masih kosong atau tulisan "sesuai harapan".** Harus hasil nyata.
4. **Screenshot dari mockup/desain**, bukan aplikasi berjalan.
5. **Video tanpa temuan statistik** atau tanpa keterbatasan → kehilangan poin eksplisit.
6. **`.env` atau kata sandi ikut terkirim.**
7. **README gagal di mesin bersih** (lupa `migrate`, lupa `seed`, path salah).
8. **Nama ZIP tidak sesuai format** → sering dinilai administratif.
9. **Dokumen dalam bahasa campur** tanpa alasan; gunakan Bahasa Indonesia konsisten.
10. **Tidak ada pembagian peran anggota** — brief menilai kerja kelompok, bukan hanya hasil.

---

## 5. Urutan pengemasan yang disarankan

1. Bekukan kode (`git tag v1.0`), jalankan `ruff check`, pastikan `DEBUG=False` untuk
   percobaan demo publik.
2. Ekspor PDF dari `docs/` (semua dokumen digabung, diagram sudah menjadi gambar).
3. Ambil ulang screenshot final dari versi `v1.0`.
4. Rekam video dari versi `v1.0`, simpan cadangan.
5. Isi semua kolom `[diisi setelah pengujian]` dan status TC.
6. Perbarui `README.md` (akun demo, langkah, troubleshooting).
7. Bersihkan artefak: `__pycache__/`, `.venv/`, `db.sqlite3`, `media/` berisi data uji
   pribadi; sertakan hanya data demo yang aman.
8. Buat ZIP, lalu lakukan uji mesin bersih (§2).
9. Unggah, lalu **unduh kembali** berkas yang diunggah dan buka satu file untuk memastikan
   tidak korup.

---

## 6. Tanda tangan kesiapan

| Anggota | Memeriksa bagian | Tanggal | Tanda tangan |
|---------|------------------|---------|--------------|
| Ridwan Rasyid | Semua dokumen, screenshot, video, ZIP | | |

> **TODO:** isi setelah semua kotak tercentang. Checklist yang ditandatangani (bahkan
> sederhana) menunjukkan proses kontrol kualitas — nilai tambah kecil yang mudah.
