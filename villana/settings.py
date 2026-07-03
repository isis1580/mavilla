"""
Django settings for villana project.
"""

from pathlib import Path
import os
import sys
from dotenv import load_dotenv
import dj_database_url
import cloudinary
import dj_database_url
# =========================
# BASE DIRECTORY
# =========================
BASE_DIR = Path(__file__).resolve().parent.parent
load_dotenv(BASE_DIR / '.env')

# =========================
# SECURITY
# =========================
SECRET_KEY = os.getenv("DJANGO_SECRET_KEY", "dev-secret-change-in-production")
DEBUG = 'RENDER' not in os.environ  # False sur Render, True en local

# Hosts autorisés
ALLOWED_HOSTS = os.getenv("DJANGO_ALLOWED_HOSTS", "127.0.0.1,localhost").split(",")

# Render fournit automatiquement un hostname externe
RENDER_EXTERNAL_HOSTNAME = os.getenv('RENDER_EXTERNAL_HOSTNAME')
if RENDER_EXTERNAL_HOSTNAME:
    ALLOWED_HOSTS.append(RENDER_EXTERNAL_HOSTNAME)

# =========================
# APPLICATIONS
# =========================
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
 
    
    # Third party
    'rest_framework',
    'rest_framework_simplejwt',
    'corsheaders',
    'cloudinary',
    'cloudinary_storage',
    
    # Local apps
    'maison',  # ton app principale
]

# =========================
# CLOUDINARY
# =========================
DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

cloudinary.config(
    cloud_name=os.getenv("CLOUDINARY_CLOUD_NAME", "dwg9lwgyt"),
    api_key=os.getenv("CLOUDINARY_API_KEY", "222745575696657"),
    api_secret=os.getenv("CLOUDINARY_API_SECRET", "ZCwHe5JOFdOMrT12A1m7d911WY4"),
    secure=True
)

# =========================
# MIDDLEWARE
# =========================
MIDDLEWARE = [
    'corsheaders.middleware.CorsMiddleware',  # Au début
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'maison.views.SimpleDebugMiddleware',
]
# =========================
# URLS & TEMPLATES
# =========================
ROOT_URLCONF = 'villana.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [BASE_DIR / 'frontend/templates'],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'villana.wsgi.application'

# =========================
# DATABASE (PostgreSQL sur Render)
# =========================
DATABASES = {
    'default': dj_database_url.config(
        default=os.getenv('DATABASE_URL'),
        conn_max_age=600,
        ssl_require=True  # Important pour Render
    )
}
# =========================
# PASSWORD VALIDATION
# =========================
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# =========================
# AUTHENTICATION
# =========================
AUTH_USER_MODEL = 'maison.User'
AUTHENTICATION_BACKENDS = [
    'django.contrib.auth.backends.ModelBackend',
    'maison.backends.MultiFieldAuthenticationBackend',
]

# =========================
# INTERNATIONALIZATION
# =========================
LANGUAGE_CODE = 'fr-fr'  # Changé pour français
TIME_ZONE = 'Africa/Douala'  # Fuseau horaire du Cameroun
USE_I18N = True
USE_TZ = True

# =========================
# STATIC & MEDIA (Important pour Render)
# =========================
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'
STATICFILES_DIRS = [
    BASE_DIR / 'frontend/static',
]
# Media files (stockés sur Cloudinary)
MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'


# Empêche le build d'échouer sur Render à cause des fichiers .map manquants de Flutter
WHITENOISE_MANIFEST_STRICT = False


# =========================
# CORS Configuration
# =========================
CORS_ALLOW_ALL_ORIGINS = True  # Autoriser tout en développement
CORS_ALLOW_CREDENTIALS = True

# Liste explicite pour la sécurité et CSRF
ALLOWED_ORIGINS_LIST = [
    "http://localhost:8000",
    "http://localhost:5761",
    "http://127.0.0.1:8000",
    "https://mavilla.onrender.com",
]

# Ajouter les origines de l'ENV
env_origins = os.getenv("CORS_ALLOWED_ORIGINS", "").split(",")
for o in env_origins:
    if o.strip():
        ALLOWED_ORIGINS_LIST.append(o.strip())

CORS_ALLOWED_ORIGINS = list(set(ALLOWED_ORIGINS_LIST))

CORS_ALLOW_HEADERS = [
    'accept',
    'accept-encoding',
    'authorization',
    'content-type',
    'dnt',
    'origin',
    'user-agent',
    'x-csrftoken',
    'x-requested-with',
    'x-expo-version',
]

# CSRF trusted origins
CSRF_TRUSTED_ORIGINS = [origin for origin in CORS_ALLOWED_ORIGINS if origin.startswith('https://')]
if "http://127.0.0.1:8000" not in CSRF_TRUSTED_ORIGINS:
    CSRF_TRUSTED_ORIGINS.append("http://127.0.0.1:8000")
# =========================
# REST FRAMEWORK
# =========================
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticatedOrReadOnly',
    ],
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 20,
    'DEFAULT_FILTER_BACKENDS': [
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# =========================
# SIMPLE JWT
# =========================
from datetime import timedelta

SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=7),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=30),
    'ROTATE_REFRESH_TOKENS': True,
    'BLACKLIST_AFTER_ROTATION': True,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
}

# =========================
# SECURITY SETTINGS (pour production)
# =========================
if not DEBUG:
    # Security settings pour Render
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')
    SECURE_SSL_REDIRECT = True
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_BROWSER_XSS_FILTER = True
    SECURE_CONTENT_TYPE_NOSNIFF = True
    SECURE_HSTS_SECONDS = 31536000  # 1 year
    SECURE_HSTS_INCLUDE_SUBDOMAINS = True
    SECURE_HSTS_PRELOAD = True
else:
    # En développement
    SECURE_SSL_REDIRECT = False
    SESSION_COOKIE_SECURE = False
    CSRF_COOKIE_SECURE = False

# =========================
# DEFAULT PK
# =========================
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# =========================
# LOGGING
# =========================
LOGGING = {
    "version": 1,
    "disable_existing_loggers": False,
    "handlers": {
        "console": {
            "class": "logging.StreamHandler",
        },
    },
    "root": {
        "handlers": ["console"],
        "level": "INFO" if DEBUG else "WARNING",
    },
    "loggers": {
        "django": {
            "handlers": ["console"],
            "level": "INFO",
            "propagate": False,
        },
    },
}