# Dokumentasi Proyek SIKULIAH

**Mata Kuliah:** Rekayasa Perangkat Lunak
**Tugas:** Tugas 1 Kelompok — Pertemuan 07
**Kelompok:** Kelompok 22
**Anggota:** Ridwan Rasyid (1003260037) — dikerjakan mandiri

---

## Cara memakai dokumen ini

1. Semua teks di dalam `[kurung siku]` adalah **placeholder** — ganti dengan data kelompok.
2. Semua teks di dalam blok `> **TODO:**` adalah **instruksi kerja**, bukan isi dokumen.
   Hapus blok TODO setelah bagian tersebut benar-benar dikerjakan.
3. Dokumen ini adalah **sumber tunggal** untuk penyusunan PDF akhir. Jangan menulis
   versi paralel di Google Docs — nanti isinya berbeda dan penilaian "dokumentasi sesuai
   implementasi" akan jatuh.
4. Diagram ditulis dengan **Mermaid** agar bisa di-render di GitHub/VS Code. Untuk PDF
   akhir, ekspor diagram menjadi PNG (draw.io / mermaid.live) lalu tempel sebagai gambar
   dengan caption `Gambar X.Y — Judul`.
5. Setelah aplikasi selesai, jalankan pemeriksaan akhir dengan
   [`11-checklist-pengumpulan.md`](11-checklist-pengumpulan.md).

## Urutan baca & status

| No | Dokumen | Isi | Dipakai untuk bagian PDF | Status |
|----|---------|-----|--------------------------|--------|
| 00 | [Identitas & Rencana Proyek](00-identitas-dan-rencana-proyek.md) | Identitas kelompok, jadwal, tools | Cover, bab 1 | ✅ |
| 01 | [Latar Belakang & Tujuan](01-latar-belakang-dan-tujuan.md) | Masalah, tujuan, manfaat, ruang lingkup | Bab 1 | ✅ |
| 02 | [Stakeholder & Hak Akses](02-stakeholder-dan-hak-akses.md) | Aktor, kebutuhan, matriks izin | Bab 2 | ✅ |
| 03 | [SRS](03-SRS.md) | FR, NFR, data, batasan, kriteria penerimaan | Bab 3 | ✅ |
| 04 | [Rancangan Sistem](04-rancangan-sistem.md) | Use case, flowchart, ERD, arsitektur, wireframe | Bab 4 | ✅ |
| 05 | [Model Pengembangan](05-model-pengembangan.md) | Prototyping + alasan + penerapan tahapan | Bab 5 | ✅ |
| 06 | [Manajemen Risiko](06-manajemen-risiko.md) | 6 risiko + dampak + mitigasi | Bab 6 | ✅ |
| 07 | [Rencana & Hasil Pengujian](07-rencana-dan-hasil-pengujian.md) | TC-01…TC-08, bug log, rekap | Bab 7 | ✅ |
| 08 | [Matriks Keterlacakan](08-matriks-keterlacakan.md) | FR → desain → kode → uji → screenshot | Lampiran | ✅ |
| 09 | [Teknologi & Struktur Kode](09-teknologi-dan-struktur-kode.md) | Stack, alasan, struktur folder, konvensi | Bab 8 | ✅ |
| 10 | [Panduan Screenshot & Video](10-panduan-screenshot-dan-video.md) | Shot list, storyboard, temuan statistik | Bab 9 + video | ✅ |
| 11 | [Checklist Pengumpulan](11-checklist-pengumpulan.md) | Paket ZIP, uji mesin bersih | — | ✅ |

Seluruh dokumen sudah ditinjau dan disesuaikan dengan implementasi pada 25 November 2026.
Sisa pekerjaan ada pada kolom bukti (video, ZIP) — lihat dokumen 10 dan 11.

## Membangun PDF

```bash
python docs/build/build_pdf.py
```

Menghasilkan `docs/build/Dokumentasi-Proyek.pdf` (sampul + daftar isi + 12 bab).
Skrip ini merender diagram Mermaid menjadi PNG melalui layanan kroki.io (butuh internet
saat build pertama). Hasilnya di-cache di `docs/build/img/`, sehingga build berikutnya
tidak memanggil jaringan lagi. Bila render gagal, blok diagram ditampilkan sebagai kode
sumber dan perlu diekspor manual dari mermaid.live.

Sampul sudah berisi Kelompok 22, Ridwan Rasyid (1003260037), dan November 2026.

## Konvensi penomoran yang dipakai lintas dokumen

| Kode | Arti |
|------|------|
| `FR-xx` | Kebutuhan fungsional (Functional Requirement) |
| `NFR-xx` | Kebutuhan nonfungsional |
| `UC-xx` | Use case |
| `TC-xx` | Test case |
| `R-xx` | Risiko |
| `BR-xx` | Aturan bisnis (business rule) |
| `A-xx` | Asumsi |

Aturan: **satu ID tidak boleh berubah arti**. Kalau sebuah fitur dibatalkan, tandai
`(dibatalkan)` — jangan pakai ulang ID-nya. Ini yang membuat matriks keterlacakan tetap sah.

## Struktur folder proyek (target)

```
UTS/
├── README.md                  ← README pengumpulan
├── docs/                      ← dokumen ini (sumber PDF)
│   ├── README.md
│   ├── 00-… s.d. 11-…
│   └── build/                 ← hasil build PDF + gambar diagram
├── src/                       ← proyek Django (dibuat pada tahap implementasi)
├── screenshots/
├── requirements.txt
├── .env.example
└── .gitignore
```

> **TODO:** folder `src/`, `screenshots/` belum ada karena implementasi belum dimulai.
> Buat saat mulai coding, jangan mengubah nama folder setelah dokumen ini diserahkan.
