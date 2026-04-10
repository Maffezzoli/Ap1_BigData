import os
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent


# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/6.0/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'django-insecure-l*%(zaptuxj!lc)ab&%)y5!5w7mxu_+&h=6!y@c2&fgt2*5a-0'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True if os.getenv('DJANGO_DEBUG', 'True') == 'True' else False

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'rest_framework',
    'produtos',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'catalogo.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'catalogo.wsgi.application'

# Configuração do banco de dados
# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases

USE_RDS = os.getenv('USE_RDS', 'False') == 'True'

if USE_RDS and os.getenv('RDS_HOSTNAME'):
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.postgresql',
            'NAME': os.getenv('RDS_DB_NAME', 'catalogodb'),
            'USER': os.getenv('RDS_USERNAME', 'catalogo_admin'),
            'PASSWORD': os.getenv('RDS_PASSWORD', ''),
            'HOST': os.getenv('RDS_HOSTNAME', ''),
            'PORT': os.getenv('RDS_PORT', '5432'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.sqlite3',
            'NAME': BASE_DIR / 'db.sqlite3',
        }
    }

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

LANGUAGE_CODE = 'pt-br'

TIME_ZONE = 'America/Sao_Paulo'

USE_I18N = True

USE_TZ = True

# Configuração de arquivos de mídia
# SQLite não suporta S3, mas já preparamos o caminho
if DEBUG:
    # Armazenamento local para desenvolvimento
    MEDIA_URL = '/media/'
    MEDIA_ROOT = os.path.join(BASE_DIR, 'media')
else:
    # Configuração preparada para S3 (será ativada depois)
    USE_S3 = os.getenv('USE_S3', 'False') == 'True'
    if USE_S3:
        # Configurações S3 serão ativadas posteriormente
        pass
    else:
        MEDIA_URL = '/media/'
        MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Hosts permitidos (importante para Elastic Beanstalk)
ALLOWED_HOSTS = os.getenv(
    'DJANGO_ALLOWED_HOSTS',
    'localhost,127.0.0.1,.elasticbeanstalk.com'
).split(',')

# Arquivos estáticos para deploy
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'