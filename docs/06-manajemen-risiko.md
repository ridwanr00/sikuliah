# 06 — Manajemen Risiko

Skala: **Peluang** dan **Dampak** 1–5. Skor = Peluang × Dampak.
Prioritas: 15–25 = tinggi, 8–14 = sedang, 1–7 = rendah.

## 1. Register risiko

| ID | Risiko | Kategori | Peluang | Dampak | Skor | Prioritas | Mitigasi (pencegahan) | Kontingensi (bila terjadi) | Pemilik |
|----|--------|----------|:-------:|:------:|:----:|-----------|------------------------|----------------------------|---------|
| R-01 | Scope creep: fitur bertambah (chat, presensi, mobile) sehingga fitur utama tidak selesai | Lingkup | 4 | 5 | 20 | **Tinggi** | Ruang lingkup dibekukan di SRS §6; fitur baru hanya boleh masuk daftar "saran pengembangan"; backlog dikunci setelah M3 | Hentikan fitur tambahan, alihkan semua anggota ke fitur utama yang belum selesai | Ketua |
| R-02 | Anggota tidak dapat berkontribusi (sakit, ujian lain, pekerjaan) | Sumber daya | 3 | 4 | 12 | Sedang | Setiap modul punya pemilik + satu pengganti; kode di-commit harian agar tidak ada pengetahuan tunggal; tugas dipecah ≤ 1 hari | Turunkan cakupan non-inti (FR-09/FR-10), bagi ulang tugas pada rapat darurat | Ketua |
| R-03 | Kehilangan data atau kode (laptop rusak, folder terhapus) | Teknis | 2 | 5 | 10 | Sedang | Repositori GitHub + commit harian; basis data demo dapat dibangun ulang via `seed_demo`; berkas unggahan tidak dianggap data permanen | Pulihkan dari commit terakhir; regenerasi data demo; jika perlu, ulangi pengujian terdampak | Backend |
| R-04 | Kebocoran kredensial / konfigurasi sensitif masuk repositori | Keamanan | 3 | 4 | 12 | Sedang | `.env` di `.gitignore`; hanya `.env.example` yang di-commit; `DEBUG=False` saat demo publik; periksa `git log -p` sebelum rilis | Rotasi `SECRET_KEY` dan kata sandi demo; hapus dari riwayat git; ganti akun yang terdampak | Backend |
| R-05 | Validasi unggah berkas tidak memadai (ekstensi palsu, berkas sangat besar) | Keamanan / Teknis | 4 | 3 | 12 | Sedang | Validasi ekstensi + MIME + ukuran di form **dan** view; batas 5 MB; nama berkas diacak; simpan di luar direktori statis | Nonaktifkan unggahan sementara, tambahkan validasi, uji ulang TC-04 | Backend |
| R-06 | Demonstrasi gagal saat presentasi (server mati, data kosong, jaringan kampus) | Operasional | 3 | 5 | 15 | **Tinggi** | Uji aplikasi di mesin presentasi H-1; video demo direkam sebagai cadangan; data demo di-seed; jalankan lokal tanpa internet (Bootstrap/Chart.js disimpan lokal) | Putar video rekaman; gunakan tangkapan layar; jelaskan alur dengan diagram | Semua |
| R-07 | Dokumentasi tidak sesuai implementasi (fitur diganti, screenshot lama) | Kepatuhan | 4 | 4 | 16 | **Tinggi** | Matriks keterlacakan diperbarui setiap siklus; screenshot diambil ulang setelah UI final; PDF dibangun dari `docs/` di commit yang sama dengan kode | Audit silang FR ↔ halaman ↔ TC sebelum kumpul; hapus klaim fitur yang tidak ada | Semua |
| R-08 | Kesalahan penilaian tenggat akibat zona waktu klien | Teknis | 2 | 3 | 6 | Rendah | Bandingkan `timezone.now()` server dengan `due_at`; set `TIME_ZONE='Asia/Jakarta'`, `USE_TZ=True` | Perbaiki data uji, dokumentasikan sebagai temuan pengujian | Backend |
| R-09 | Pengerjaan mandiri: tidak ada anggota kedua untuk meninjau kode, menguji, atau menggantikan saat kehabisan waktu | Sumber daya | 3 | 5 | 15 | **Tinggi** | Bekukan lingkup (P0/P1/P2, dokumen 00 §3.2); commit setiap 30 menit; uji di folder bersih; minta satu orang luar mencoba alur submit | Potong P1, jaga P0 tetap utuh; gunakan panel admin Django untuk CRUD; rekam video cadangan lebih awal | Ketua |

**Jumlah risiko: 9** (brief mensyaratkan minimal 3). Empat teratas (R-01, R-07, R-06, R-09)
adalah yang paling mungkin terjadi pada proyek akademik dan wajib disebut saat presentasi.

## 2. Ringkasan visual (matriks peluang–dampak)

| Dampak ↓ / Peluang → | 1 | 2 | 3 | 4 | 5 |
|---|:--:|:--:|:--:|:--:|:--:|
| **5** | | R-03 | R-06, R-09 | | R-01 |
| **4** | | | R-02, R-04 | R-07 | |
| **3** | | R-08 | | R-05 | |
| **2** | | | | | |
| **1** | | | | | |

## 3. Rencana pemantauan

| Waktu | Aktivitas | Bukti |
|-------|-----------|-------|
| Awal setiap siklus | Tinjau register: ada risiko baru? skor berubah? | Catatan rapat 5 baris |
| Akhir setiap siklus | Periksa apakah risiko yang dimitigasi benar-benar hilang | Hasil demo + screenshot |
| Sebelum pengumpulan | Audit R-07 (dokumentasi vs implementasi) | Checklist dokumen 11 |
| Saat presentasi | Siapkan cadangan R-06 | Video + data demo siap |

## 4. Risiko yang diterima (tidak dimitigasi penuh)

| Risiko | Alasan diterima | Dampak yang disadari |
|--------|-----------------|----------------------|
| Tidak ada backup otomatis basis data | Skala demo, data dapat diregenerasi | Kehilangan data uji maksimal satu sesi |
| Tidak ada pengujian beban nyata | Di luar ruang lingkup akademik | Klaim performa dibatasi pada "diuji manual, bukan uji beban" (ditulis di keterbatasan) |
| Tidak ada audit keamanan pihak ketiga | Keterbatasan waktu dan kompetensi | Dinyatakan sebagai keterbatasan sistem, bukan jaminan keamanan produksi |

> **TODO:** tambahkan satu risiko yang benar-benar terjadi selama pengerjaan (mis. anggota
> sakit, fitur terlambat) beserta tindakan yang diambil. Risiko nyata yang terdokumentasi
> lebih meyakinkan daripada daftar teoretis.
