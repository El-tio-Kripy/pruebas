from pathlib import Path

# Ruta base del proyecto
BASE_DIR = Path(__file__).resolve().parent.parent

# Clave secreta (solo para desarrollo)
SECRET_KEY = "cambia-esta-clave-antes-de-produccion"

# Modo debug activado para desarrollo
DEBUG = True

ALLOWED_HOSTS: list[str] = []

# Aplicaciones instaladas
INSTALLED_APPS = [
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",

    # Apps del proyecto Eva2 / Eva3
    "eva2LopezJorge_app",
    "eva2Trabajador_app",
    "Eva3Api",

    # Django REST Framework y tokens
    "rest_framework",
    "rest_framework.authtoken",
]

# Middleware de Django
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

ROOT_URLCONF = "eva2LopezJorge_prj.urls"

# Configuración de templates (por ahora sin carpeta global)
TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [
            # BASE_DIR / "templates",  # descomentar si luego agregas plantillas globales
        ],
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

# Aplicación WSGI
WSGI_APPLICATION = "eva2LopezJorge_prj.wsgi.application"

# Configuración de la base de datos (MariaDB/MySQL con mysql-connector)
DATABASES = {
    "default": {
        "ENGINE": "mysql.connector.django",
        'NAME': 'eva3LopezJorge',
        "USER": "root",
        "PASSWORD": "root",
        "HOST": "localhost",
        "PORT": "3309",
        "OPTIONS": {
            "init_command": "SET sql_mode='STRICT_TRANS_TABLES'",
        },
    }
}

# Configuración regional
LANGUAGE_CODE = "es-cl"
TIME_ZONE = "America/Santiago"
USE_I18N = True
USE_TZ = True

# Archivos estáticos
STATIC_URL = "/static/"
STATICFILES_DIRS = [BASE_DIR / "static"]

DEFAULT_AUTO_FIELD = "django.db.models.BigAutoField"

# Configuración de Django REST Framework
REST_FRAMEWORK = {
    "DEFAULT_AUTHENTICATION_CLASSES": [
        "rest_framework.authentication.TokenAuthentication",
        "rest_framework.authentication.SessionAuthentication",
    ],
    "DEFAULT_PERMISSION_CLASSES": [
        "rest_framework.permissions.IsAuthenticated",
    ],
    "DEFAULT_PAGINATION_CLASS": "rest_framework.pagination.PageNumberPagination",
    "PAGE_SIZE": 10,
}

# A dónde mandar al usuario DESPUÉS de hacer login en /api-auth/login/
LOGIN_URL = "/api-auth/login/"
LOGIN_REDIRECT_URL = "/api/"
# (si quisieras que vaya al admin en vez de /api/, cambia a: LOGIN_REDIRECT_URL = "/admin/")
