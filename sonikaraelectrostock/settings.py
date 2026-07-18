from pathlib import Path
import dotenv
import os


# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent
dotenv.load_dotenv(BASE_DIR / '.env')

# variable pour determiné si on est prod
PRODUCTION = os.environ.get('ENV', 'production') == 'production'

SECRET_KEY = os.environ.get('SECRET_KEY')

DEBUG = os.environ.get('DEBUG', 'False') == "True"

ALLOWED_HOSTS = os.environ.get("ALLOWED_HOSTS").split(',') if PRODUCTION else ['*']


# Application definition

INSTALLED_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'accounts',
    'dashboard',
    'stores',
    'products',
    'stocks',
    'purchases',
    'suppliers',
    'customers',
    'sales',
    'payments',
    'documents',
    'quotes',
    'credits',
    'expenses',


    # autre app
    'django.contrib.humanize',
    'django_user_agents',
    'rest_framework',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django_user_agents.middleware.UserAgentMiddleware',
    'sonikaraelectrostock.middleware.DesktopOnlyMiddleware',

    "whitenoise.middleware.WhiteNoiseMiddleware",
]

ROOT_URLCONF = 'sonikaraelectrostock.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': ['templates'],
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

WSGI_APPLICATION = 'sonikaraelectrostock.wsgi.application'


# Database
# https://docs.djangoproject.com/en/6.0/ref/settings/#databases
# DATABASES = {
#     'default': {
#         'ENGINE': 'django.db.backends.sqlite3',
#         'NAME': BASE_DIR / 'db.sqlite3',
#     }
# }

if PRODUCTION:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_SONI_DB'),
            'USER': os.getenv('MYSQL_SONI_USER'),
            'PASSWORD': os.getenv('MYSQL_SONI_PASSWORD'),
            'HOST': os.getenv('MYSQL_SONI_HOST'),
            'PORT': os.getenv('MYSQL_SONI_PORT'),
        }
    }
else:
    DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'NAME': os.getenv('MYSQL_LOCAL_DB'),
            'USER': os.getenv('MYSQL_LOCAL_USER'),
            'PASSWORD': os.getenv('MYSQL_LOCAL_PASSWORD'),
            'HOST': os.getenv('MYSQL_LOCAL_HOST'),
            'PORT': os.getenv('MYSQL_LOCAL_PORT'),
        }
    }


# Password validation
# https://docs.djangoproject.com/en/6.0/ref/settings/#auth-password-validators

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



AUTH_USER_MODEL = 'accounts.CustomUser'
AUTHENTICATION_BACKENDS = ['accounts.backends.EmailBackend']

# Internationalization
# https://docs.djangoproject.com/en/6.0/topics/i18n/

LANGUAGE_CODE = 'fr-fr'

TIME_ZONE = 'Africa/Bamako'

USE_I18N = True

USE_TZ = True


STATIC_URL = '/static/'
MEDIA_URL = "/media/"

STATICFILES_DIRS = [
    BASE_DIR / "static",
]


MEDIA_ROOT = BASE_DIR / "media"
STATIC_ROOT = BASE_DIR / 'staticfiles'




LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,

    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(lineno)s %(message)s',
        },

        'simple': {
            'format': '%(levelname)s %(message)s',
        },
    },

    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse',
        },
    },

    'handlers': {
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename' :  os.path.join(BASE_DIR, 'logs/debug.log'),
            'formatter': 'verbose'
        },
        'info': {
            'filename' :  os.path.join(BASE_DIR, 'logs/info.log'),
            'filters': ['require_debug_false'],
            'class': 'logging.handlers.RotatingFileHandler',
            'formatter': 'verbose',
            'backupCount' : 5,
            'maxBytes' : 1024*1024*50,
            'encoding' : 'utf8',
            'level': 'INFO',
        },
    },

    'loggers': {
        'django': {
            'handlers':['file'],
            'propagate': True,
            'level':'DEBUG',
        },
        'info_log': {
            'handlers': ['info'],
            'level': 'INFO',
            'propagate': True
        },
    }
}