#!/usr/bin/env bash
# Build untuk hosting (Render/Railway): pasang dependensi dan kumpulkan statis.
set -o errexit

pip install -r requirements.txt
cd src
python manage.py check          # gagal cepat bila ada dependensi kurang
python manage.py collectstatic --noinput
