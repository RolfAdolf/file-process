from .base import *


# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = False

ADMINS = [
    (
        settings.django_superuser_username,
        settings.django_superuser_email
    ),
]

ALLOWED_HOSTS = ['*']

# Database
# https://docs.djangoproject.com/en/4.2/ref/settings/#databases
DATABASES = {
    "default": {
        "ENGINE": "django.db.backends.postgresql",
        "NAME": settings.postgres_db,
        "USER": settings.postgres_user,
        "PASSWORD": settings.postgres_password,
        "HOST": settings.postgres_host,
        "PORT": settings.postgres_port,
    }
}

CELERY_BROKER_URL='amqp://guest:guest@rabbitmq3:5672/'
