from pathlib import Path
from datetime import timedelta
from os.path import join

from decouple import config


BASE_DIR = Path(__file__).resolve().parent.parent


# Load env vars
DEBUG = config('DEBUG', default=False, cast=bool)
SECRET_KEY = config('SECRET_KEY')
# POSTGRES_PASSWORD = config('POSTGRES_PASSWORD')
CS__ALLOWED_HOSTS = config('CS__ALLOWED_HOSTS')
CS__CORS_ORIGIN_WHITELIST = config('CS__CORS_ORIGIN_WHITELIST')
DJANGO_TIME_ZONE = config('DJANGO_TIME_ZONE')
DJANGO_LANGUAGE_CODE = config('DJANGO_LANGUAGE_CODE')


# AllowedHosts and CORS
ALLOWED_HOSTS=["*"] if DEBUG else CS__ALLOWED_HOSTS.split(',')

CORS_ORIGIN_ALLOW_ALL = DEBUG
CORS_ORIGIN_WHITELIST = CS__CORS_ORIGIN_WHITELIST.split(',')


ROOT_URLCONF = "kaizntree_backend.urls"

INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "djmoney",
    "rest_framework",
    "rest_framework_simplejwt",
    "rest_framework_simplejwt.token_blacklist",
    "dashboard_api",
]

SERIALIZATION_MODULES = {
    "json": "djmoney.serializers",
}

MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [],
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

CACHES = {
    "default": {
        "BACKEND": "django_redis.cache.RedisCache",
        "LOCATION": "redis://127.0.0.1:6379/1",
        "OPTIONS": {
            "CLIENT_CLASS": "django_redis.client.DefaultClient",
        }
    }
}

WSGI_APPLICATION = "kaizntree_backend.wsgi.application"


# Database
DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# DATABASES = {
#     "default": {
#         "ENGINE": "django.db.backends.postgresql",
#         "NAME": "postgres",
#         "USER": "postgres",
#         "HOST": "localhost",
#         "PASSWORD": POSTGRES_PASSWORD,
#         "PORT": 5432,
#     }
# }
# Use Sqlite for testing locally
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.sqlite3",
        "NAME": join(BASE_DIR, "db.sqlite3"),
    }
}


# Authentication
AUTH_USER_MODEL = "dashboard_api.CustomUser"

AUTH_PASSWORD_VALIDATORS = [
    {"NAME": "django.contrib.auth.password_validation.UserAttributeSimilarityValidator",},
    {"NAME": "django.contrib.auth.password_validation.MinimumLengthValidator",},
    {"NAME": "django.contrib.auth.password_validation.CommonPasswordValidator",},
    {"NAME": "django.contrib.auth.password_validation.NumericPasswordValidator",},
]


# Language and Time Zone
LANGUAGE_CODE = DJANGO_LANGUAGE_CODE
TIME_ZONE = DJANGO_TIME_ZONE
USE_I18N = True
USE_TZ = True


# DRF
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ],
}


# DRF Simple JWT
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(days=15) if DEBUG else timedelta(minutes=15),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=90),

    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
    'USER_AUTHENTICATION_RULE': 'rest_framework_simplejwt.authentication.default_user_authentication_rule',

    'AUTH_TOKEN_CLASSES': ('rest_framework_simplejwt.tokens.AccessToken',),
    'TOKEN_TYPE_CLAIM': 'token_type',
    'TOKEN_USER_CLASS': 'rest_framework_simplejwt.models.TokenUser',

    'JTI_CLAIM': 'jti',
}


# Static and Media
STATIC_URL = '/static/'
STATIC_ROOT = join(BASE_DIR, 'static')

MEDIA_URL= "/media/"
MEDIA_ROOT = join(BASE_DIR, "media")
