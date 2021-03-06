from corsheaders.defaults import default_headers

from polyaxon.utils import ROOT_DIR, config

DEBUG = config.get_boolean('POLYAXON_DEBUG')

ALLOWED_HOSTS = ['*']

# session settings
CORS_ORIGIN_ALLOW_ALL = True
CORS_ALLOW_CREDENTIALS = True

SSL_ENABLED = config.get_boolean('POLYAXON_SSL_ENABLED', is_optional=True, default=False)
CORS_ORIGIN_WHITELIST = config.get_string('POLYAXON_CORS_ORIGIN_WHITELIST', is_optional=True)
if CORS_ORIGIN_WHITELIST:
    CORS_ORIGIN_WHITELIST = [i.strip() for i in CORS_ORIGIN_WHITELIST.split(',')]
else:
    CORS_ORIGIN_WHITELIST = []

CORS_ALLOW_HEADERS = default_headers + (
    'x-polyaxon-cli-version',
    'x-polyaxon-client-version',
)

if SSL_ENABLED:
    SESSION_COOKIE_SECURE = True
    CSRF_COOKIE_SECURE = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')

WSGI_APPLICATION = 'polyaxon.wsgi.application'
TIME_ZONE = config.get_string('POLYAXON_TIME_ZONE', is_optional=True) or 'Europe/Berlin'
LANGUAGE_CODE = 'en'
LANGUAGES = (
    ('en', u'English'),
)

USE_I18N = True
USE_L10N = True
USE_TZ = True

INTERNAL_IPS = ('127.0.0.1',)
APPEND_SLASH = True

ROOT_URLCONF = 'polyaxon.urls'

# user management
LOGIN_URL = '/users/login/'
LOGOUT_REDIRECT_URL = LOGIN_URL
LOGIN_REDIRECT_URL = '/'
ACCOUNT_ACTIVATION_DAYS = 7
INVITATION_TIMEOUT_DAYS = 30

SESSION_COOKIE_AGE = 24 * 60 * 60  # 24 hours
SESSION_COOKIE_HTTPONLY = True

DEFAULT_DB_ENGINE = 'django.db.backends.postgresql'
DATABASES = {
    'default': {
        'ENGINE': config.get_string('POLYAXON_DB_ENGINE', is_optional=True) or DEFAULT_DB_ENGINE,
        'NAME': config.get_string('POLYAXON_DB_NAME'),
        'USER': config.get_string('POLYAXON_DB_USER'),
        'PASSWORD': config.get_string('POLYAXON_DB_PASSWORD', is_secret=True),
        'HOST': config.get_string('POLYAXON_DB_HOST'),
        'PORT': config.get_string('POLYAXON_DB_PORT'),
        'ATOMIC_REQUESTS': True,
        'CONN_MAX_AGE': config.get_int('POLYAXON_DB_CONN_MAX_AGE', is_optional=True, default=0),
    }
}

LIST_TEMPLATE_CONTEXT_PROCESSORS = [
    'django.contrib.auth.context_processors.auth',
    'django.template.context_processors.debug',
    'django.template.context_processors.i18n',
    'django.template.context_processors.media',
    'django.template.context_processors.static',
    'django.template.context_processors.tz',
    'django.contrib.messages.context_processors.messages',
    'versions.context_processors.versions',
    'clusters.context_processors.cluster',
    'sso.context_processors.sso_enabled',
]

JS_DEBUG = config.get_boolean('POLYAXON_JS_DEBUG')

if JS_DEBUG:
    def js_debug_processor(request):
        return {'js_debug': True}

    LIST_TEMPLATE_CONTEXT_PROCESSORS += ('polyaxon.settings.js_debug_processor',)

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [
            ROOT_DIR.child('polyaxon').child('polyaxon').child('templates'),
        ],
        'APP_DIRS': True,
        'OPTIONS': {
            'debug': config.get_boolean('DJANGO_TEMPLATE_DEBUG', is_optional=True) or DEBUG,
            'context_processors': LIST_TEMPLATE_CONTEXT_PROCESSORS,
        },
    },
]

POLYAXON_ENVIRONMENT = config.env

POLYAXON_NOTIFICATION_CLUSTER_ALIVE_URL = (
    "{url}&cid={cluster_uuid}&t=pageview&"
    "dp=%2Fplatform%2F{cluster_uuid}"
    "%2F{create_at}%2F{version}&"
    "ds=app&z={notification}&"
    "an=polyaxon&aid=com.polyaxon.app&av={version}")

POLYAXON_NOTIFICATION_CLUSTER_NODES_URL = (
    "{url}&cid={cluster_uuid}&t=pageview&"
    "dp=%2Fplatform%2F{cluster_uuid}%2F{n_nodes}"
    "%2F{n_cpus}%2F{memory}%2F{n_gpus}%2F{version}&"
    "ds=app&z={notification}&"
    "an=polyaxon&aid=com.polyaxon.app&av={version}")
