from .base import *
#change debug, localhost, database

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': config("DB_NAME_DEV"),
        'USER': config("DB_USER_DEV"),
        'PASSWORD': config("DB_PASSWORD_DEV"),
        'HOST': config("DB_HOST_DEV"),
        'PORT': config("DB_PORT_DEV", cast=int),
    }
}
