from os import getenv
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

BASE_DIR = Path(__file__).resolve().parent.parent

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = getenv('SECRET_KEY')

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = getenv('DEBUG') == 'True'

ALLOWED_HOSTS = getenv('ALLOWED_HOSTS', 'localhost, 127.0.0.1').split(', ')

CSRF_TRUSTED_ORIGINS = getenv(
    'CSRF_TRUSTED_ORIGINS',
    'https://127.0.0.1, https://localhost, '
    'https://www.127.0.0.1, https://www.localhost'
).split(', ')

# Application definition
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'core',
    'games',
    'pages',
    'purchases',
    'users',

    'debug_toolbar',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

INTERNAL_IPS = ['127.0.0.1']

ROOT_URLCONF = 'gamedi.urls'

AUTH_USER_MODEL = 'users.User'

LOGIN_URL = 'login'

LOGIN_REDIRECT_URL = 'games:home'

CSRF_FAILURE_VIEW = 'pages.views.csrf_failure'

WSGI_APPLICATION = 'gamedi.wsgi.application'


# Database
DATABASES = {
    'default': {
        'ENGINE': getenv('ENGINE'),
        'NAME': getenv('POSTGRES_DB'),
        'USER': getenv('POSTGRES_USER'),
        'PASSWORD': getenv('POSTGRES_PASSWORD'),
        'HOST': getenv('DB_HOST'),
        'PORT': getenv('DB_PORT'),
    }
}


# Static files (HTML, CSS, JavaScript, Images)
STATIC_URL = 'static/'
STATIC_DIR = BASE_DIR / 'static'
STATIC_ROOT = BASE_DIR / 'staticfiles'

STATICFILES_DIRS = [STATIC_DIR]

MEDIA_URL = '/media/'
MEDIA_ROOT = BASE_DIR / 'media'

TEMPLATES_DIR = STATIC_DIR / 'templates'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [TEMPLATES_DIR],
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


# Password validation
AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]


# Internationalization
LANGUAGE_CODE = 'ru-RU'

TIME_ZONE = 'Europe/Moscow'

USE_I18N = True

USE_TZ = True


# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'


# Email
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
# DEFAULT_FROM_EMAIL = getenv('DEFAULT_FROM_EMAIL')
# EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EMAIL_USE_TLS = getenv('EMAIL_USE_TLS')
# EMAIL_HOST = getenv('EMAIL_HOST')
# EMAIL_HOST_USER = getenv('EMAIL_HOST_USER')
# EMAIL_HOST_PASSWORD =getenv('EMAIL_HOST_PASSWORD')
# EMAIL_PORT = getenv('EMAIL_PORT')


# YooKassa
ID_YOOKASSA = getenv('ID_YOOKASSA')
SECRET_KEY_YOOKASSA = getenv('SECRET_KEY_YOOKASSA')
