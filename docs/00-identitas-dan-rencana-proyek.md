# 00 — Identitas Kelompok & Rencana Proyek

## 1. Identitas kelompok

| Item | Keterangan |
|------|------------|
| Nama kelompok | Kelompok 22 |
| Judul tugas | SIKULIAH — Learning Management System Kampus Berbasis Web |
| Topik | Sistem informasi pendidikan / learning management system |
| Mata kuliah | Rekayasa Perangkat Lunak |
| Kelas | IF119 - Rekayasa Perangkat Lunak |
| Dosen | Anas Nasrulloh, S.Kom., M.Kom. |
| Institusi | Institut Teknologi Tangerang Selatan |
| Tanggal mulai | 19 November 2026 |
| Tanggal pengumpulan | 26 November 2026 |

### Anggota dan pembagian peran

| No | Nama | NIM | Peran utama | Tanggung jawab |
|----|------|-----|-------------|----------------|
| 1 | Ridwan Rasyid | 1003260037 | Ketua, analis kebutuhan, desainer, backend, QA | SRS dan seluruh dokumen, rancangan & wireframe, implementasi Django, pengujian, video, pengemasan |

> **Catatan administratif:** brief menetapkan 2–3 anggota per kelompok, sedangkan proyek ini
> dikerjakan mandiri. Simpan bukti persetujuan dosen (chat/email) dan cantumkan satu baris
> keterangan di sampul PDF: "Dikerjakan mandiri atas persetujuan dosen pengampu." Ini
> mencegah penilaian administratif yang tidak perlu.

## 2. Ringkasan proyek

SIKULIAH adalah aplikasi web untuk mengelola kegiatan perkuliahan satu program studi:
dosen mengunggah materi dan tugas, mahasiswa mengumpulkan tugas, dosen menilai dan memberi
umpan balik, serta admin mengelola pengguna dan mata kuliah. Aplikasi menyediakan dasbor
statistik sederhana (jumlah mahasiswa per mata kuliah, tingkat pengumpulan tugas, distribusi
nilai) sebagai dasar evaluasi perkuliahan.

- **Fitur utama 1:** pengelolaan dan distribusi materi pembelajaran (FR-05).
- **Fitur utama 2:** pengumpulan tugas daring beserta penilaian dan umpan balik (FR-06, FR-07, FR-08).

## 3. Jadwal kerja (19–26 November 2026)

Proyek dikerjakan mandiri dalam 8 hari kalender (± 3 hari kerja efektif). Tabel ini adalah
**rencana** yang menjadi dasar laporan — isi kolom status sesuai kenyataan, jangan menulis
selesai untuk hal yang belum dikerjakan.

| Tanggal | Fokus | Keluaran | Status |
|---------|-------|----------|--------|
| 19 Nov | Ruang lingkup & stakeholder | Dokumen 01–02 | ✅ |
| 20–21 Nov | SRS & rancangan | Dokumen 03–05, diagram, wireframe | ✅ |
| 22–23 Nov | Fondasi aplikasi | Proyek Django, model, seeder, auth + RBAC, base template | ✅ |
| 24 Nov | Fitur utama | Materi (FR-05), tugas & pengumpulan (FR-06/07), penilaian (FR-08) | ✅ |
| 25 Nov | Statistik, pengujian, perbaikan | Dasbor (FR-10), TC-01…TC-08, bug log | ✅ |
| 26 Nov | Pengemasan | Screenshot final, video, PDF, README, ZIP + uji mesin bersih | 🟡 |

### 3.1 Rencana sisa waktu (25–26 November)

Urutan ini disusun agar **setiap jam menghasilkan bahan yang dinilai**, bukan pekerjaan yang
bisa dipotong di menit terakhir.

| Slot | Aktivitas | Keluaran wajib |
|------|-----------|----------------|
| 25 Nov, 1 jam | Bekukan lingkup: tandai FR yang dikerjakan vs dicoret di SRS | Daftar P0/P1/P2 (§3.2) |
| 25 Nov, 4–5 jam | Bangun inti Django: model + migrasi + seeder, login/RBAC, materi, tugas, submit, nilai | Aplikasi jalan, 2 fitur utama berfungsi |
| 25 Nov, 1 jam | Dasbor statistik + perapian template/base | Grafik dari data nyata |
| 25 Nov, 1 jam | Eksekusi TC-01…TC-08, isi hasil aktual + screenshot | Tabel uji terisi, 6–8 gambar |
| 26 Nov, 1 jam | Perbaiki bug dari TC, uji ulang yang gagal | Bug log dengan status |
| 26 Nov, 1,5 jam | Rekam video 3 menit 30 detik sesuai naskah dokumen 10 | `Video Presentasi_Kelompok 22.mp4` |
| 26 Nov, 2 jam | Isi dokumen, build PDF, lengkapi README | `Dokumentasi-Proyek.pdf` |
| 26 Nov, 1 jam | ZIP + uji mesin bersih + unggah | ZIP terverifikasi |

Aturan: **aplikasi dulu, penyempurnaan dokumen belakangan.** Dokumen sudah 90% siap; yang
belum ada adalah aplikasi, dan tanpa aplikasi tidak ada screenshot, hasil uji, atau video.

### 3.2 Triage: apa yang dipotong bila waktu tidak cukup

| Prioritas | Cakupan | Aturan |
|-----------|---------|--------|
| **P0 — wajib** | Login + RBAC 3 peran, materi unggah/unduh, tugas + pengumpulan + penilaian, dasbor statistik sederhana, 5 TC, 4 screenshot, video, PDF, ZIP | Tidak boleh dipotong. Ini yang secara eksplisit dinilai brief. |
| **P1 — kalau ada waktu** | Pengumuman (FR-09), pencarian, halaman 403/404 kustom, edit/hapus materi, responsif detail | Kerjakan hanya setelah P0 lulus uji. |
| **P2 — jangan dikerjakan** | Registrasi mandiri, profil, reset kata sandi via surel, multi-dosen, ekspor Excel | Catat di "saran pengembangan", bukan dikerjakan. |

Penghemat waktu terbesar: **kelola pengguna dan mata kuliah lewat panel admin Django**
(`/admin`) yang sudah memiliki pencarian, filter peran, dan validasi. Itu tetap memenuhi
FR-02/FR-03 dan menghemat 3–4 jam pembuatan UI CRUD. Cantumkan keputusan ini di SRS sebagai
catatan implementasi, bukan disembunyikan.

### Milestone

| Milestone | Target | Kriteria selesai |
|-----------|--------|------------------|
| M1 — Baseline dokumen | 21 Nov | SRS + rancangan final, semua ID kebutuhan dibekukan |
| M2 — Aplikasi berjalan lokal | 24 Nov | Login 3 peran, mata kuliah & materi berfungsi |
| M3 — Fitur utama lengkap | 25 Nov | Submit tugas + penilaian berjalan, dasbor terisi data nyata |
| M4 — Siap kumpul | 26 Nov (pagi) | 8 TC tereksekusi, PDF, video ≥ 3 menit, ZIP lolos uji mesin bersih |

> **TODO:** setelah pengujian, ubah kolom Status pada tabel §3 menjadi ✅/🟡/⬜ sesuai
> kenyataan. Jadwal yang jujur (termasuk yang terlambat) lebih aman daripada jadwal sempurna
> yang tidak cocok dengan tanggal commit di repositori.

## 4. Tools

| Kebutuhan | Tool | Alasan |
|-----------|------|--------|
| Manajemen tugas | GitHub Issues / Trello | Riwayat pekerjaan terlihat |
| Repositori kode | GitHub (privat) | Backup + kolaborasi + histori commit |
| Diagram | draw.io (use case, arsitektur) + mermaid.live (flowchart, sequence) | Ekspor PNG untuk PDF |
| ERD | dbdiagram.io | Ekspor PNG + SQL |
| Wireframe | Figma | Prototipe klik untuk validasi awal |
| Editor kode | VS Code | Ekstensi Python + Django |
| Dokumentasi | Markdown di repo ini | Sumber tunggal, mudah di-diff |
| Rekaman video | OBS Studio | 1080p, kursor terlihat |
| Konversi PDF | LibreOffice / Word dari hasil ekspor | Pastikan font tertanam |

## 5. Aturan kerja tim

1. **Satu sumber kebenaran:** dokumen di folder `docs/` mengalahkan chat. Kalau ada
   perubahan keputusan, ubah dokumennya di commit yang sama.
2. **Branch:** `main` (stabil) ← `dev` ← `feat/<nama-fitur>`. Tidak ada commit langsung
   ke `main` selain rilis.
3. **Commit:** `feat(materi): tambah unggah materi`, `fix(tugas): tolak submit lewat deadline`.
4. **Rahasia:** `.env` tidak pernah di-commit. Yang di-commit hanya `.env.example`.
5. **Definisi selesai (DoD) sebuah fitur:**
   - berjalan di `main` lokal,
   - lolos validasi input (kasus kosong, salah format, terlalu besar),
   - otorisasi diuji untuk peran yang tidak berhak,
   - minimal 1 TC terkait tercatat,
   - screenshot tersimpan di `screenshots/`,
   - baris matriks keterlacakan diperbarui.
6. **Tidak menambah fitur baru setelah M3** kecuali Fitur Utama yang belum berfungsi.
   Fitur tambahan dicatat di bagian "Saran Pengembangan", bukan dikerjakan.

## 6. Batasan waktu yang disepakati

Proyek ini sengaja dibatasi pada **satu program studi, satu semester, satu kelas per mata
kuliah**. Integrasi SIAKAD, pembayaran, video conference, dan aplikasi mobile **di luar
ruang lingkup** dan dinyatakan eksplisit di SRS bab 6 supaya tidak dinilai sebagai
kekurangan implementasi.
