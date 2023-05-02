"""
Django settings for ai_web project.

Generated by 'django-admin startproject' using Django 4.1.5.

For more information on this file, see
https://docs.djangoproject.com/en/4.1/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/4.1/ref/settings/
"""
import environ
import os
from pathlib import Path
from django.utils.translation import gettext_lazy as _

# 2023-05-02 10:39 phamhung20022015
# [Note]: Lưu ý các đoạn code được comment ở dưới là optional
# vi lý do hầu hết là khiến hiệu năng của trang giảm nên phải
# tắt đi, trong tương lai nếu muốn active thì cần nghiên cứu kĩ lại
# để tránh làm hỏng code cũ.

env = environ.Env(
    # set casting, default value
    DEBUG=(bool, False)
)

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Take environment variables from .env file
environ.Env.read_env(os.path.join(BASE_DIR, ".env"))
ENVIRONMENT = env("ENVIRONMENT", default="development")

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/4.1/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!

SECRET_KEY = env("SECRET_KEY")

# SECURITY WARNING: don't run with debug turned on in production!

DEBUG = env("DEBUG")

ALLOWED_HOSTS = ["*"]

# Application definition

INSTALLED_APPS = [
    "sslserver",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "home.apps.HomeConfig",
    "blog.apps.BlogConfig",
    "about.apps.AboutConfig",
    "contact.apps.ContactConfig",
    # Third-party
    "debug_toolbar",
    "ckeditor",
    "ckeditor_uploader",
]

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "whitenoise.middleware.WhiteNoiseMiddleware",  # Whitenoise helps to serve staticfiles in production
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
    "debug_toolbar.middleware.DebugToolbarMiddleware",
]

ROOT_URLCONF = "ai_web.urls"

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(BASE_DIR, "templates")],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
            ],
        },
    },
]

WSGI_APPLICATION = "ai_web.wsgi.application"


# Database
# https://docs.djangoproject.com/en/4.1/ref/settings/#databases

DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": os.path.join(BASE_DIR, "db.sqlite3"),
    }
}


# Password validation
# https://docs.djangoproject.com/en/4.1/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",
    },
    {
        "NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",
    },
]


# Internationalization
# https://docs.djangoproject.com/en/4.1/topics/i18n/

LANGUAGE_CODE = "en-us"

LANGUAGES = [
    ("de", _("German")),
    ("en", _("English")),
    ("vi", _("Vietnam")),
]

TIME_ZONE = "UTC"

USE_I18N = True

USE_TZ = True

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/4.1/howto/static-files/
STATIC_URL = "/static/"

STATIC_ROOT = BASE_DIR / "productionfiles/"

# Default primary key field type
# https://docs.djangoproject.com/en/4.1/ref/settings/#default-auto-field
# Prevent add uploads file to the repo
STATICFILES_DIRS = [os.path.join(BASE_DIR, "static")]

MEDIA_URL = "/media/"
MEDIA_ROOT = os.path.join(BASE_DIR, "static/uploads")

# Supporting for forever-cacheable files and compression
# More details: https://whitenoise.readthedocs.io/en/stable/django.html
# 2023-04-29 14:02 phamhung20022015@gmail.com
# [Note]: Enable storage will fail `python manage.py test`
#  STORAGES = {
#      "staticfiles": {
#          "BACKEND": "whitenoise.storage.CompressedManifestStaticFilesStorage",
#      },
#  }

# Rich text editor with ckeditor
CKEDITOR_UPLOAD_PATH = "uploads/"

CKEDITOR_CONFIGS = {
    "default": {"toolbar": "full", "height": 300, "width": "100%"},
}

CKEDITOR_STORAGE_BACKEND = "django.core.files.storage.FileSystemStorage"


# production
if ENVIRONMENT == "production":
    DEBUG = False
    SECURE_BROWSER_XSS_FILTER = True  # prevent cross-site scripting(XSS) attack
    X_FRAME_OPTIONS = "DENY"  # prevent clickjacking attack
    SECURE_HSTS_SECONDS = 3600
    SECURE_HSTS_INCLUDE_SUBDOMAINS = (
        True  # force any subdomains to also exclusively use SSL
    )
    SECURE_HSTS_PRELOAD = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SESSION_COOKIE_SECURE = True
    #  CSRF_COOKIE_SECURE = True
    #  CSRF_TRUSTED_ORIGINS = ["https://*.railway.app", "https://www.*.railway.app"]

    #  [Note]: 2023-04-29 13:43 phamhung20022015@gmail.com
    #  Khi triển khai trang lên server thì 2 tùy chỉnh dưới đây sẽ tăng bảo mật nhưng sẽ đánh đổi
    #  về mặt độ trễ khi chuyển trang. Trong trường hợp yêu cầu cao về bảo mật nếu ko thì nên False
    #  để giúp trang load nhanh hơn.
    #  SECURE_PROXY_SSL_HEADER = ("HTTP_X_FORWARDED_PROTO", "https") # prevent browsers from using the website on insecure HTTP connections.
    #  SECURE_SSL_REDIRECT = True  # force all non-HTTPS traffic to be redirected to HTTPS


# django-debug-toolbar
if DEBUG:
    import socket  # only if you haven't already imported this

    hostname, _, ips = socket.gethostbyname_ex(socket.gethostname())
    INTERNAL_IPS = [ip[: ip.rfind(".")] + ".1" for ip in ips] + [
        "127.0.0.1",
        "10.0.2.2",
    ]
