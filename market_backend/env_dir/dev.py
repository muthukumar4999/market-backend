from .base import *
import dj_database_url

DEBUG = True

ALLOWED_HOSTS = ["*"]

# Database
# https://docs.djangoproject.com/en/2.1/ref/settings/#databases
try:
    from .databases import DBCONFIG

except ModuleNotFoundError:
    DATABASES = {'default': {'ENGINE': 'django.db.backends.postgresql_psycopg2',
                             'NAME': 'market',
                             'HOST': 'localhost',
                             'PORT': 5432,
                             'USER': 'dev',
                             'PASSWORD': 'dev',
                             'ATOMIC_REQUESTS': True,
                             }
                 }
else:
    DATABASES = DBCONFIG
    DATABASES['default']['ATOMIC_REQUESTS'] = True

db_from_env = dj_database_url.config(conn_max_age=500)
DATABASES['default'].update(db_from_env)

EMAIL_HOST_USER = ''
EMAIL_HOST_PASSWORD = ''

AWS_BUCKET_NAME = os.environ.get('AWS_BUCKET_NAME', 'mr-sbs')
AWS_ACCESS_KEY = os.environ.get('AWS_ACCESS_KEY', 'AKIAIMV5CDFIT32UNOLQ')
AWS_SECRET_ACCESS_KEY = os.environ.get('AWS_SECRET_ACCESS_KEY', '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')
AWS_REGION_NAME = os.environ.get('AWS_REGION_NAME', 'us-east-1')

AWS_S3_BASE_LINK = "https://s3.amazonaws.com/{}/".format(AWS_BUCKET_NAME)