# config/settings.py
import os
import dj_database_url
import cloudinary
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configurações de Segurança ---
SECRET_KEY = os.environ.get('SECRET_KEY')
DEBUG = os.environ.get('DEBUG') == '1'

ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',')] if ALLOWED_HOSTS_ENV else []

# --- Configurações da Aplicação ---
INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic',
    'django.contrib.staticfiles',
    
    # Apps de terceiros
    'cloudinary',

    # Nossos apps
    'core.apps.CoreConfig',
    'products.apps.ProductsConfig',
    'designs.apps.DesignsConfig',
    'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

ROOT_URLCONF = 'config.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'orders.context_processors.cart_context',
            ],
        },
    },
]

WSGI_APPLICATION = 'config.wsgi.application'

DATABASES = {'default': dj_database_url.config(conn_max_age=600)}

AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- Estáticos (CSS, JS) ---
# Esta configuração não muda. Whitenoise continua a ser a melhor opção.
STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

# --- Mídia (Uploads) ---
# A nova biblioteca lê a STORAGE_URL. Se não existir, usa o padrão local.
# Defina uma variável STORAGE_URL no Heroku com o mesmo valor da sua CLOUDINARY_URL.
STORAGE_CONFIG = dj_storage_url.config()
DEFAULT_FILE_STORAGE = STORAGE_CONFIG.get('BACKEND')
MEDIA_URL = STORAGE_CONFIG.get('URL')
MEDIA_ROOT = STORAGE_CONFIG.get('ROOT')
    
# --- Tipos de campo padrão ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'contatoy@premiumgrafica.com.br'