# 12 — Basis Data Online, Koneksi dari Komputer, dan Cadangan

Dokumen ini menjawab tiga hal: **menyimpan data agar tidak hilang** saat aplikasi
di-hosting, **menghubungkan basis data ke komputer** (DBeaver/pgAdmin/psql), dan
**membuat serta memulihkan cadangan**.

---

## 1. Masalah: SQLite di hosting gratis bersifat sementara

Aplikasi berjalan di Render dengan SQLite (`src/db.sqlite3`). Pada paket gratis Render,
disk bersifat **ephemeral**: berkas hilang setiap deploy ulang atau restart instance.
Akibatnya:

- pengguna dan nilai yang dibuat saat demo bisa hilang;
- berkas materi dan pengumpulan (folder `media/`) ikut hilang;
- `seed_demo` dijalankan lagi saat start, sehingga data kembali ke kondisi awal.

Kode aplikasi **tidak** bermasalah karena tersimpan di GitHub. Yang perlu dipindahkan
adalah **basis data** (dan, bila perlu, berkas unggahan).

## 2. Arsitektur yang dituju

```text
Peramban  →  Render (Django + gunicorn)  →  Neon Postgres (persisten)
                        ↓
             media/ (masih sementara — lihat §6)
```

| Komponen | Tempat | Persisten? |
|----------|--------|------------|
| Kode aplikasi | GitHub | ✅ |
| Basis data | Neon Postgres (gratis) | ✅ |
| Berkas unggahan (`media/`) | Disk Render | ❌ (hilang saat redeploy) |
| Statis (CSS/JS) | Dibundel `collectstatic` | ✅ (ikut build) |

Alternatif Neon: Supabase (Postgres), Railway, atau Render Postgres berbayar.
Hindari database gratis yang punya masa berlaku (mis. paket gratis yang dihapus setelah
beberapa minggu), karena data bisa hilang tepat saat penilaian.

---

## 3. Pindah ke Neon (sekali saja, ± 10 menit)

1. Buka <https://neon.tech> → daftar dengan GitHub.
2. **Create project**:
   - Name: `sikuliah`
   - Postgres version: default
   - Region: **Singapore (ap-southeast-1)** — terdekat ke Indonesia/Render Singapore.
3. Setelah project dibuat, buka **Connection details** dan salin **Connection string**
   (mode *Pooled connection*). Bentuknya:

   ```text
   postgresql://neondb_owner:PASSWORD@ep-xxxx-pooler.ap-southeast-1.aws.neon.tech/neondb?sslmode=require
   ```

4. Buka Render → service `sikuliah` → **Environment** → **Add Environment Variable**:

   | Key | Value |
   |-----|-------|
   | `DATABASE_URL` | connection string dari Neon (jangan dibagikan) |

5. **Manual Deploy → Deploy latest commit** (atau tunggu auto-deploy).
   Perintah start sudah menjalankan `migrate` lalu `seed_demo`, sehingga tabel dibuat
   dan data demo langsung terisi pada basis data baru.
6. Verifikasi: buka situs, login `dosen1@kampus.test / dosen12345`, lalu cek angka
   dasbor. Lakukan satu pengumpulan tugas, kemudian **restart** service dari dashboard
   Render — data harus tetap ada.

> **Catatan:** koneksi *pooled* dipakai untuk aplikasi web. Untuk klien desktop
> (DBeaver), gunakan koneksi **direct** (tanpa `-pooler`) agar fitur seperti
> `pg_dump` dan inspeksi skema berjalan normal.

---

## 4. Melihat basis data dari komputer

### 4.1 Data koneksi

Ambil dari Neon → **Connection details → Direct connection**:

| Field | Nilai (contoh) |
|-------|----------------|
| Host | `ep-xxxx.ap-southeast-1.aws.neon.tech` |
| Port | `5432` |
| Database | `neondb` |
| User | `neondb_owner` |
| Password | (dari connection string) |
| SSL | **Wajib** (`require` / `verify-full`) |

### 4.2 DBeaver (disarankan, gratis)

1. Install DBeaver Community → **Database → New Database Connection → PostgreSQL**.
2. Isi Host, Port, Database, Username, Password.
3. Tab **SSL** → centang **Use SSL**, mode `require` (atau `verify-full`).
4. **Test Connection** → Finish.
5. Jelajahi: `public → tables`. Tabel penting: `accounts_user`, `courses_course`,
   `assignments_assignment`, `assignments_submission`, `materials_material`.

Alternatif cepat: di DBeaver pilih **URL** lalu tempel connection string Neon lengkap.

### 4.3 pgAdmin

**Register → Server** → tab *Connection*: isi host/port/database/user; tab *SSL*:
SSL mode `require`. Simpan dengan password.

### 4.4 Terminal (`psql`)

```bash
psql "postgresql://neondb_owner:PASSWORD@ep-xxxx.ap-southeast-1.aws.neon.tech/neondb?sslmode=require"
```

Query yang berguna:

```sql
SELECT role, count(*) FROM accounts_user GROUP BY role;
SELECT a.title, count(s.id) AS terkumpul, round(avg(s.score),1) AS rata_rata
FROM assignments_assignment a
LEFT JOIN assignments_submission s ON s.assignment_id = a.id
GROUP BY a.id ORDER BY a.due_at DESC;
```

### 4.5 Akun baca-saja (disarankan untuk presentasi)

Jangan pakai `neondb_owner` saat sekadar melihat data. Buat akun terbatas:

```sql
CREATE ROLE pengamat LOGIN PASSWORD 'ganti-dengan-password-panjang';
GRANT CONNECT ON DATABASE neondb TO pengamat;
GRANT USAGE ON SCHEMA public TO pengamat;
GRANT SELECT ON ALL TABLES IN SCHEMA public TO pengamat;
ALTER DEFAULT PRIVILEGES IN SCHEMA public GRANT SELECT ON TABLES TO pengamat;
```

Gunakan akun ini di DBeaver. Akun ini tidak bisa mengubah atau menghapus data.

---

## 5. Cadangan (backup) dan pemulihan

### 5.1 Tiga lapis cadangan

| Lapis | Cara | Kapan |
|-------|------|-------|
| Kode | GitHub + tag rilis (`git tag v1.0 && git push --tags`) | setiap rilis |
| Basis data | `scripts/backup.sh` (pg_dump / dumpdata) | sebelum demo & harian |
| Riwayat otomatis | Fitur *restore* bawaan Neon (window terbatas pada paket gratis) | saat darurat |

### 5.2 Menjalankan cadangan

```bash
# dari root proyek; DATABASE_URL dibaca dari .env atau src/.env
scripts/backup.sh
```

Hasil di `backups/<tanggal-jam>/`:

- `database.dump` — dump Postgres (bila `pg_dump` terpasang; install `postgresql-client`),
- `data.json` — cadangan `dumpdata` bila `pg_dump` tidak ada,
- `media.tar.gz` — berkas unggahan (bila ada di mesin ini).

### 5.3 Cadangan harian otomatis (Linux/macOS)

```bash
crontab -e
# tambahkan (sesuaikan path):
0 22 * * * cd "/path/ke/UTS" && scripts/backup.sh >> backups/backup.log 2>&1
```

Salin folder `backups/` ke Google Drive/OneDrive minimal sekali sehari. Cadangan yang
hanya ada di laptop yang sama bukan cadangan.

### 5.4 Memulihkan

```bash
scripts/restore.sh backups/20261125-2200/database.dump   # Postgres
scripts/restore.sh backups/20261125-2200/data.json       # alternatif JSON
```

`pg_restore` menimpa tabel yang ada. Untuk Neon, cara paling aman saat presentasi:
buat **branch** baru di Neon (fitur *branches*) lalu arahkan `DATABASE_URL` ke branch
tersebut, sehingga basis data utama tidak tersentuh sampai yakin.

### 5.5 Uji cadangan (wajib sekali)

Cadangan yang belum pernah dipulihkan belum bisa dipercaya. Lakukan sekali:

1. `scripts/backup.sh`
2. Restore ke database kosong (branch Neon baru).
3. Buka aplikasi dengan `DATABASE_URL` branch tersebut, pastikan jumlah pengguna dan
   nilai sama.

---

## 6. Berkas unggahan (`media/`) masih hilang saat redeploy

Basis data sudah aman, tetapi berkas materi/pengumpulan tetap di disk sementara Render.
Pilihan:

| Pilihan | Usaha | Catatan |
|---------|-------|---------|
| Terima apa adanya | 0 | Cocok untuk demo: unggah ulang berkas bila perlu. Sebutkan sebagai keterbatasan. |
| Supabase Storage (S3-compatible) | ± 45 menit | Gratis 1 GB; pakai `django-storages` + `boto3`, set `AWS_*` dan `STORAGES`. |
| Cloudinary | ± 30 menit | Gratis 25 GB; butuh `cloudinary` + `django-cloudinary-storage`; cocok untuk gambar/PDF. |
| Render Disk (berbayar) | ± 10 menit | Hanya pada instance berbayar; mount ke `/var/data`, set `MEDIA_ROOT`. |

Langkah ringkas Supabase Storage (bila dipilih):

1. Buat project Supabase → **Storage → New bucket** `media` (private).
2. **Project Settings → API**: catat `SUPABASE_URL`, `SUPABASE_SERVICE_KEY`, region.
3. `pip install django-storages[boto3]`.
4. Set env: `AWS_S3_ENDPOINT_URL=https://<project>.supabase.co/storage/v1/s3`,
   `AWS_STORAGE_BUCKET_NAME=media`, `AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`,
   `AWS_S3_REGION_NAME`.
5. Ubah `STORAGES["default"]` ke `storages.backends.s3.S3Storage` bila env tersedia.
6. Uji unggah materi, lalu restart service — berkas harus tetap dapat diunduh.

---

## 7. Keamanan

1. `DATABASE_URL` hanya disimpan sebagai environment variable (Render) dan `.env`
   lokal yang masuk `.gitignore`. Jangan pernah menempelkannya di README, screenshot,
   atau video.
2. Jangan tampilkan dashboard Neon/DBeaver berisi password saat merekam video.
3. Ganti kata sandi akun demo setelah penilaian, atau hapus service.
4. Batasi akun yang bisa menulis: aplikasi memakai satu user DB; manusia memakai
   akun `pengamat` (baca-saja).
5. Aktifkan 2FA pada akun GitHub, Render, dan Neon.

---

## 8. Troubleshooting

| Gejala | Penyebab | Solusi |
|--------|----------|--------|
| `ssl connection is required` | URL tanpa `sslmode` | Tambahkan `?sslmode=require` |
| `too many connections` | Memakai koneksi direct dari banyak worker | Gunakan host `-pooler` untuk aplikasi |
| `relation ... does not exist` | `migrate` belum jalan | Deploy ulang (start command menjalankan migrate) atau `python manage.py migrate` dengan `DATABASE_URL` diset |
| Data kembali kosong setelah restart | `DATABASE_URL` belum diset di Render | Set env, deploy ulang, cek `SELECT count(*) FROM accounts_user` |
| DBeaver tidak bisa konek | Port/SSL salah atau memakai host pooler | Pakai koneksi direct + SSL `require` |
| `pg_dump: command not found` | Klien PostgreSQL belum ada | `sudo apt install postgresql-client` atau pakai `data.json` |

---

## 9. Checklist sebelum presentasi

- [ ] `DATABASE_URL` terpasang di Render dan data bertahan setelah restart.
- [ ] DBeaver dapat terhubung memakai akun `pengamat`.
- [ ] `scripts/backup.sh` menghasilkan `database.dump`/`data.json`.
- [ ] Cadangan disalin ke cloud (Drive/OneDrive).
- [ ] Satu kali uji restore berhasil.
- [ ] Keterbatasan `media/` disebutkan di laporan dan video.
