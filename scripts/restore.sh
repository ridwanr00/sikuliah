#!/usr/bin/env bash
# Pulihkan basis data dari hasil scripts/backup.sh
#
# Pemakaian:
#   scripts/restore.sh backups/20261125-1600/database.dump
#   scripts/restore.sh backups/20261125-1600/data.json
#
# PERINGATAN: restore menimpa data yang ada. Pastikan sudah punya cadangan terbaru.

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

if [ -z "${DATABASE_URL:-}" ]; then
  echo "DATABASE_URL belum diisi." >&2
  exit 1
fi

FILE="${1:-}"
if [ -z "$FILE" ] || [ ! -f "$FILE" ]; then
  echo "Pemakaian: scripts/restore.sh <berkas .dump atau .json>" >&2
  exit 1
fi

case "$FILE" in
  *.dump)
    command -v pg_restore >/dev/null 2>&1 || {
      echo "pg_restore tidak terpasang (install postgresql-client)." >&2
      exit 1
    }
    pg_restore --clean --if-exists --no-owner --dbname="$DATABASE_URL" "$FILE"
    ;;
  *.json)
    (
      cd src
      ../.venv/bin/python manage.py loaddata "../$FILE"
    )
    ;;
  *)
    echo "Format tidak dikenal. Gunakan .dump atau .json" >&2
    exit 1
    ;;
esac

echo "restore selesai dari $FILE"
