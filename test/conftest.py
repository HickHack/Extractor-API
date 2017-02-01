"""
This is the test setup file which is
run before any tests and it used to
configure django so it can be tests
can be executed using pytest
"""

import os
import django
from django.conf import settings

# Manually set django settings environment variable
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'extractor_api.settings')
os.environ['ENV'] = 'TEST'


def pytest_configure():
    settings.ENV = 'TEST'
    settings.DEBUG = False
    settings.DATABASES = {
        'default': {
            'ENGINE': 'django.db.backends.mysql',
            'USER': 'root',
            'PASSWORD': '',
            'HOST': '127.0.0.1',
            'PORT': '3306',
            'TEST': {
                'NAME': 'extractor_service_test',
            },
        }
    }

    django.setup()
