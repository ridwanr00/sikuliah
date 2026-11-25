# 05 — Model Pengembangan Perangkat Lunak

## 1. Model yang dipilih: Prototyping (evolutionary)

Proyek dikembangkan dengan **Prototyping evolusioner** dalam empat siklus. Setiap siklus
menghasilkan versi aplikasi yang benar-benar dapat dijalankan, dievaluasi oleh anggota
kelompok (mewakili pengguna), lalu diperbaiki pada siklus berikutnya.

### Alasan pemilihan

| Pertimbangan | Penjelasan |
|--------------|------------|
| Kebutuhan awal belum stabil | Kebutuhan tampilan (mis. bentuk tabel penilaian, penempatan tombol unduh) baru jelas setelah dilihat. Prototipe memungkinkan koreksi murah. |
| Waktu sangat terbatas (19–26 November, ± 3 hari kerja efektif) | Siklus pendek 2–6 jam memberi hasil yang bisa didemokan lebih awal, bukan satu rilis besar di hari deadline. |
| Tim kecil (2–3 orang) | Tidak perlu upacara Scrum lengkap (sprint planning formal, daily standup, dsb.). Prototyping cukup dengan backlog + evaluasi akhir siklus. |
| Risiko utama = ketidaksesuaian UI dengan kebutuhan | Prototipe menyerang risiko itu paling awal, bukan di akhir. |
| Butuh bukti "aplikasi benar-benar berjalan" | Setiap siklus meninggalkan versi yang dapat dijalankan dan di-screenshot, sehingga bahan dokumentasi terkumpul bertahap. |

### Model yang tidak dipilih dan alasannya
- **Waterfall** — dokumen dan desain beku di awal; perubahan kecil pada formulir berarti
  revisi besar. Tidak cocok untuk proyek akademik dengan tenggat pendek dan UI yang belum
  disepakati.
- **Scrum penuh** — peran (Product Owner, Scrum Master), artefak, dan ritualnya berlebihan
  untuk tim 2–3 orang; sebagian prinsipnya tetap dipakai (backlog, increment, retrospektif).
- **RAD / JAD** — membutuhkan keterlibatan pengguna nyata secara intensif; dosen dan
  mahasiswa tidak tersedia untuk sesi kerja bersama.

## 2. Tahapan dan penerapannya

| Tahap | Aktivitas | Keluaran | Siklus |
|-------|-----------|----------|--------|
| 1. Komunikasi & analisis kebutuhan | Wawancara singkat, studi brief, penyusunan FR/NFR | Dokumen 01, 02, 03 | Pra-siklus (19–21 Nov) |
| 2. Perencanaan cepat | Menyusun backlog fitur, memilih isi siklus, menetapkan DoD | Backlog + jadwal siklus | Setiap awal siklus |
| 3. Pemodelan & desain cepat | Use case, ERD, wireframe, arsitektur | Dokumen 04 | Siklus 1 |
| 4. Pembentukan prototipe | Implementasi fitur siklus, migrasi basis data, template | Kode berjalan | Siklus 1–4 |
| 5. Penyerahan & evaluasi | Demo internal, uji cepat, catat temuan | Daftar perbaikan + screenshot | Akhir setiap siklus |
| 6. Penyempurnaan | Perbaikan hasil evaluasi, lalu masuk siklus berikutnya | Versi increment | Siklus 2–4 |
| 7. Rekayasa akhir | Pengujian formal TC-01…TC-08, dokumentasi, pengemasan | Dokumen 07, PDF, ZIP | 25–26 Nov |

## 3. Rincian siklus

### Siklus 1 — Fondasi dan akses (22–23 November)
- **Isi:** proyek Django, model `User` + peran, login/logout, RBAC, pengelolaan pengguna &
  mata kuliah melalui panel admin Django, enrollment, layout dasar + navigasi.
- **Demo:** admin membuat mata kuliah lewat `/admin`; mahasiswa mendaftar; dosen hanya
  melihat mata kuliahnya.
- **Kriteria evaluasi:** tiga peran dapat login dan melihat menu berbeda; URL terlarang
  menghasilkan 403.
- **Risiko yang dimatikan:** struktur proyek berantakan, otorisasi bocor.
- **Keputusan penghemat waktu:** UI CRUD pengguna/mata kuliah memakai panel admin Django
  (sudah menyediakan pencarian, filter, dan validasi) — menghemat 3–4 jam.

### Siklus 2 — Fitur Utama 1: materi (24 November, pagi)
- **Isi:** unggah/ubah/hapus materi, validasi berkas, unduh materi, halaman materi
  mahasiswa, breadcrumb dan keadaan kosong.
- **Demo:** dosen mengunggah PDF; mahasiswa mengunduh; berkas 6 MB ditolak.
- **Kriteria evaluasi:** unduhan identik dengan berkas asli; mahasiswa non-peserta 403.
- **Risiko yang dimatikan:** validasi unggah lemah, path traversal.

### Siklus 3 — Fitur Utama 2: tugas, pengumpulan, penilaian (24 November, siang–malam)
- **Isi:** CRUD tugas, tenggat + status otomatis, pengumpulan berkas (upsert), daftar
  pengumpulan, formulir nilai + umpan balik, tampilan nilai mahasiswa.
- **Demo:** mahasiswa mengumpulkan; dosen menilai; mahasiswa melihat nilai.
- **Kriteria evaluasi:** submit lewat tenggat ditolak; nilai > maksimum ditolak; unggahan
  ulang menggantikan berkas, bukan menduplikasi.
- **Risiko yang dimatikan:** data ganda, nilai tidak valid, kebocoran berkas antar mahasiswa.

### Siklus 4 — Statistik, pemantapan, dan pengujian (25 November)
- **Isi:** dasbor statistik (Chart.js), halaman error kustom, responsivitas, aksesibilitas
  dasar, seeder data demo, eksekusi TC-01…TC-08.
- **Isi P1 (hanya bila P0 selesai):** pengumuman (FR-09), pencarian, penggantian berkas
  yang lebih halus.
- **Demo:** statistik terisi data nyata; tampilan 360 px tidak rusak.
- **Kriteria evaluasi:** angka dasbor cocok dengan hitung manual; tidak ada error bagi nol.
- **Risiko yang dimatikan:** demonstrasi tanpa data, tampilan rusak di ponsel.

## 4. Perbandingan dengan praktik Scrum yang tetap dipakai

| Praktik Scrum | Diterapkan? | Bentuk sederhana di proyek ini |
|---------------|-------------|-------------------------------|
| Product backlog | Ya | Daftar FR di SRS, diurutkan prioritas |
| Sprint (1–2 minggu) | Ya, sebagai siklus | Siklus 2–6 jam |
| Increment yang dapat dijalankan | Ya | Setiap akhir siklus ada versi lokal |
| Daily standup | Tidak formal | Catatan 5 baris di akhir sesi kerja |
| Sprint review | Ya | Demo internal + screenshot |
| Retrospektif | Ya | 3 pertanyaan: apa lancar, apa macet, apa diubah |

## 5. Definition of Done (dipakai di setiap siklus)

Sebuah item backlog dianggap selesai bila:
1. berjalan pada `main` lokal tanpa error konsol;
2. validasi input diuji minimal untuk kasus kosong, format salah, dan terlalu besar;
3. otorisasi diuji untuk peran yang tidak berhak;
4. minimal satu test case terkait dicatat di dokumen 07 (boleh TC manual);
5. screenshot tersimpan dengan nama sesuai dokumen 10;
6. baris matriks keterlacakan (dokumen 08) diperbarui;
7. README tidak perlu diubah, atau sudah diubah bila ada dependensi baru.

## 6. Kalender penerapan

| Tanggal | Siklus | Milestone |
|---------|--------|-----------|
| 19–21 Nov | Pra-siklus | M1 dokumen baseline dibekukan |
| 22–23 Nov | Siklus 1 | M2 aplikasi berjalan, 3 peran aktif |
| 24 Nov (pagi) | Siklus 2 | Fitur Utama 1 demo |
| 24 Nov (malam) | Siklus 3 | Fitur Utama 2 demo |
| 25 Nov | Siklus 4 | M3 fitur lengkap + data demo + TC terisi |
| 26 Nov | Pasca-siklus | M4 siap kumpul (PDF, video, ZIP) |

> **TODO:** isi jam kerja nyata. Bila sisa waktu < 12 jam, kerjakan hanya P0 pada dokumen 00
> §3.2 dan turunkan FR-09 menjadi "tidak diimplementasikan" di SRS — **jangan** menulis
> seolah sudah ada. Jangan mengorbankan Siklus 2 dan 3: keduanya fitur utama yang dinilai.

## 7. Risiko proses dan pengendaliannya

Lihat [06 — Manajemen Risiko](06-manajemen-risiko.md). Dua risiko yang paling sering
mematikan proyek prototyping adalah **scope creep** (R-01) dan **prototipe berhenti sebagai
prototipe** (tidak pernah dirapikan). Pengendaliannya: backlog dibekukan setelah M3, dan
setiap siklus wajib menyisakan satu hari untuk perapian kode serta dokumentasi.
