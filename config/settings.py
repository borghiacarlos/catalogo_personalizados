import os
import dj_database_url
from pathlib import Path

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# --- Configurações de Segurança ---

# A SECRET_KEY é lida da variável de ambiente.
SECRET_KEY = os.environ.get('SECRET_KEY')

# O modo DEBUG é Falso em produção, a menos que a variável de ambiente seja '1'.
DEBUG = os.environ.get('DEBUG') == '1'

# --- LÓGICA CORRIGIDA PARA ALLOWED_HOSTS ---
# Em produção, o Heroku nos dará uma string com o nosso domínio.
ALLOWED_HOSTS_ENV = os.environ.get('ALLOWED_HOSTS')
if ALLOWED_HOSTS_ENV:
    # Se a variável existir, dividimos a string por vírgulas para criar uma lista.
    # Isso nos permite ter múltiplos domínios no futuro, se necessário.
    ALLOWED_HOSTS = [host.strip() for host in ALLOWED_HOSTS_ENV.split(',')]
else:
    # Se a variável não existir (em desenvolvimento local), a lista fica vazia
    # e o Django adiciona 'localhost' e '127.0.0.1' automaticamente quando DEBUG=True.
    ALLOWED_HOSTS = []


# --- Configurações da Aplicação ---

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'whitenoise.runserver_nostatic', # Whitenoise
    'django.contrib.staticfiles',
    'cloudinary_storage',
    'cloudinary',
    
    # Nossos apps
    'core.apps.CoreConfig',
    'products.apps.ProductsConfig',
    'designs.apps.DesignsConfig',
    'orders.apps.OrdersConfig',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'whitenoise.middleware.WhiteNoiseMiddleware', # Whitenoise
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

# --- Configuração do Banco de Dados ---
# Usa a URL do banco de dados do Heroku (DATABASE_URL) se estiver disponível.
DATABASES = {
    'default': dj_database_url.config(
        default=f'sqlite:///{BASE_DIR / "db.sqlite3"}',
        conn_max_age=600,
        conn_health_checks=True,
    )
}

# --- Validação de Senha ---
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# --- Internacionalização ---
LANGUAGE_CODE = 'pt-br'
TIME_ZONE = 'America/Sao_Paulo'
USE_I18N = True
USE_TZ = True

# --- Configurações de Arquivos Estáticos e Mídia ---
STATIC_URL = 'static/'
STATICFILES_DIRS = [ BASE_DIR / 'static' ]
STATIC_ROOT = BASE_DIR / 'staticfiles'
STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'

MEDIA_URL = '/media/'
# Em produção, usaremos o Cloudinary. Em desenvolvimento, continuaremos usando o local.
if DEBUG:
    MEDIA_ROOT = BASE_DIR / 'media'
else:
    # Esta configuração diz ao Django para usar o Cloudinary para os uploads
    DEFAULT_FILE_STORAGE = 'cloudinary_storage.storage.MediaCloudinaryStorage'

# --- Configuração de Email ---
EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'
DEFAULT_FROM_EMAIL = 'no-reply@premiumgrafica.com.br'

# --- Tipos de campo padrão ---
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# Esta configuração será lida a partir da variável de ambiente no Heroku
CLOUDINARY_URL = os.environ.get('CLOUDINARY_URL')