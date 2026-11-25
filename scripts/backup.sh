#!/usr/bin/env bash
# Cadangkan basis data + berkas media ke folder backups/<tanggal-jam>/.
#
# Pemakaian:
#   scripts/backup.sh
#
# Sumber kredensial: variabel lingkungan DATABASE_URL (boleh dari .env di root
# atau src/.env). Jika pg_dump tidak terpasang, dipakai `manage.py dumpdata`
# (JSON) yang tidak memerlukan klien PostgreSQL.

set -euo pipefail
cd "$(dirname "$0")/.."

for env_file in .env src/.env; do
  if [ -f "$env_file" ]; then
    set -a
    # shellcheck disable=SC1090
    . "$env_file"
    set +a
  fi
done

if [ -z "${DATABASE_URL:-}" ] && [ ! -f src/db.sqlite3 ]; then
  echo "DATABASE_URL belum diisi dan src/db.sqlite3 tidak ada." >&2
  echo "Salin connection string Neon ke .env, atau jalankan dari folder proyek lokal." >&2
  exit 1
fi

STAMP="$(date +%Y%m%d-%H%M%S)"
OUT="backups/$STAMP"
mkdir -p "$OUT"

if command -v pg_dump >/dev/null 2>&1; then
  pg_dump "$DATABASE_URL" --no-owner --format=custom --file="$OUT/database.dump"
  echo "basis data  : $OUT/database.dump (format custom Postgres)"
else
  (
    cd src
    ../.venv/bin/python manage.py dumpdata \
      --natural-foreign --natural-primary \
      -e contenttypes -e auth.permission --indent 2 > "../$OUT/data.json"
  )
  echo "basis data  : $OUT/data.json (dumpdata; pasang postgresql-client untuk pg_dump)"
fi

if [ -d src/media ]; then
  tar -czf "$OUT/media.tar.gz" -C src media
  echo "media       : $OUT/media.tar.gz"
fi

echo "selesai     : $OUT"
