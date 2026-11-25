"""Konfigurasi Django untuk proyek SIKULIAH."""

from pathlib import Path

import dj_database_url
from decouple import Csv, config

BASE_DIR = Path(__file__).resolve().parent.parent

SECRET_KEY = config("DJANGO_SECRET_KEY", default="dev-only-secret-key-ganti-sebelum-demo-publik")
DEBUG = config("DJANGO_DEBUG", default=True, cast=bool)
ALLOWED_HOSTS = config("DJANGO_ALLOWED_HOSTS", default="127.0.0.1,localhost", cast=Csv())

# --- Penyesuaian hosting (Render/PythonAnywhere) ---
# Render menyetel RENDER_EXTERNAL_HOSTNAME otomatis; tambahkan tanpa perlu edit manual.
RENDER_HOST = config("RENDER_EXTERNAL_HOSTNAME", default="")
if RENDER_HOST:
    ALLOWED_HOSTS.append(RENDER_HOST)

CSRF_TRUSTED_ORIGINS = config("CSRF_TRUSTED_ORIGINS", default="", cast=Csv())
if RENDER_HOST:
    CSRF_TRUSTED_ORIGINS.append(f"https://{RENDER_HOST}")

# Render/PythonAnywhere meneruskan HTTPS lewat proxy.
SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https")

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "whitenoise.runserver_nostatic",
    "django.contrib.staticfiles",
    "apps.accounts",
    "apps.courses",
    "apps.materials",
    "apps.assignments",
    "apps.announcements",
    "apps.dashboard",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "config.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [BASE_DIR / "templates"],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "config.wsgi.application"

# Basis data: Postgres (produksi) bila DATABASE_URL diisi, SQLite untuk pengembangan.
DATABASE_URL = config("DATABASE_URL", default="")

if DATABASE_URL:
    DATABASES = {
        "default": dj_database_url.parse(
            DATABASE_URL,
            conn_max_age=600,
            conn_health_checks=True,
            ssl_require=DATABASE_URL.startswith("postgres"),
        )
    }
else:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": BASE_DIR / "db.sqlite3",
        }
    }

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator"},
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
        "OPTIONS": {"min_length": 8},
    },
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator"},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator"},
]

AUTH_USER_MODEL = "accounts.User"

LANGUAGE_CODE = "id"
TIME_ZONE = "Asia/Jakarta"
USE_I18N = True
USE_TZ = True

STATIC_URL = "static/"
STATICFILES_DIRS = [BASE_DIR / "static"]
STATIC_ROOT = BASE_DIR / "staticfiles"

MEDIA_URL = "/media/"
MEDIA_ROOT = BASE_DIR / "media"

STORAGES = {
    "default": {"BACKEND": "django.core.files.storage.FileSystemStorage"},
    "staticfiles": {"BACKEND": "whitenoise.storage.CompressedStaticFilesStorage"},
}

# --- Object storage opsional (Supabase/B2/R2) ---
# Aktifkan dengan USE_S3_STORAGE=True dan isi enam variabel di bawah.
# Tanpa itu, berkas tetap disimpan di media/ lokal (atau disk sementara Render).
USE_S3_STORAGE = config("USE_S3_STORAGE", default=False, cast=bool)

if USE_S3_STORAGE:
    AWS_ACCESS_KEY_ID = config("AWS_ACCESS_KEY_ID")
    AWS_SECRET_ACCESS_KEY = config("AWS_SECRET_ACCESS_KEY")
    AWS_STORAGE_BUCKET_NAME = config("AWS_STORAGE_BUCKET_NAME")
    AWS_S3_ENDPOINT_URL = config("AWS_S3_ENDPOINT_URL", default="")
    AWS_S3_REGION_NAME = config("AWS_S3_REGION_NAME", default="")
    AWS_S3_SIGNATURE_VERSION = "s3v4"
    # B2 dan Supabase memakai path-style (bucket di path URL), bukan virtual-host.
    # AWS asli tetap memakai virtual-host.
    AWS_S3_ADDRESSING_STYLE = config(
        "AWS_S3_ADDRESSING_STYLE",
        default="path" if AWS_S3_ENDPOINT_URL else "virtual",
    )
    AWS_DEFAULT_ACL = None          # bucket tetap privat
    AWS_QUERYSTRING_AUTH = True     # tautan sementara bertanda tangan
    AWS_S3_FILE_OVERWRITE = False
    AWS_S3_OBJECT_PARAMETERS = {"CacheControl": "private, max-age=3600"}
    STORAGES["default"] = {
        "BACKEND": "storages.backends.s3.S3Storage",
        "OPTIONS": {
            "access_key": AWS_ACCESS_KEY_ID,
            "secret_key": AWS_SECRET_ACCESS_KEY,
            "bucket_name": AWS_STORAGE_BUCKET_NAME,
            "endpoint_url": AWS_S3_ENDPOINT_URL or None,
            "region_name": AWS_S3_REGION_NAME or None,
            "default_acl": None,
            "querystring_auth": True,
            "file_overwrite": False,
            "addressing_style": AWS_S3_ADDRESSING_STYLE,
        },
    }

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

LOGIN_URL = "/masuk/"
LOGIN_REDIRECT_URL = "/dasbor/"
LOGOUT_REDIRECT_URL = "/"
SESSION_COOKIE_AGE = 60 * 60  # NFR-03: sesi berakhir setelah 60 menit
SESSION_SAVE_EVERY_REQUEST = True
SESSION_COOKIE_HTTPONLY = True
SESSION_COOKIE_SAMESITE = "Lax"
CSRF_COOKIE_SAMESITE = "Lax"

# Batas unggahan (BR-05)
MAX_UPLOAD_SIZE_MB = config("MAX_UPLOAD_SIZE_MB", default=5, cast=int)
MAX_UPLOAD_SIZE_BYTES = MAX_UPLOAD_SIZE_MB * 1024 * 1024
ALLOWED_UPLOAD_EXTENSIONS = {"pdf", "docx", "pptx", "zip"}

MESSAGE_STORAGE = "django.contrib.messages.storage.session.SessionStorage"

# Cookie aman hanya dikirim lewat HTTPS. Bisa dimatikan untuk uji produksi di localhost.
SECURE_COOKIES = config("DJANGO_SECURE_COOKIES", default=not DEBUG, cast=bool)
SESSION_COOKIE_SECURE = SECURE_COOKIES
CSRF_COOKIE_SECURE = SECURE_COOKIES

if not DEBUG:
    SECURE_CONTENT_TYPE_NOSNIFF = True
    X_FRAME_OPTIONS = "DENY"

# Redirect HTTPS & HSTS hanya aktif saat berjalan di hosting (Render).
# Di localhost dengan DEBUG=False keduanya dimatikan agar uji lokal tetap bisa.
SECURE_SSL_REDIRECT = config("DJANGO_SECURE_SSL_REDIRECT", default=bool(RENDER_HOST), cast=bool)
SECURE_HSTS_SECONDS = config("DJANGO_HSTS_SECONDS", default=3600 if RENDER_HOST else 0, cast=int)
SECURE_HSTS_INCLUDE_SUBDOMAINS = False
