'''
import os

import pytest

from django.conf import settings


@pytest.fixture(scope='session')
def django_db_modify_db_settings(django_db_modify_db_settings,):
    os.environ['ENV'] = 'test'
    settings.DATABASES['default'] = {
        'ENGINE':   'django.db.backends.sqlite3',
        'NAME':     ':memory:'
    }



def pytest_configure():
    print('### ERIC PYTEST START')
    print(settings.__dict__)
    print('### ERIC PYTEST END')

    #print('>>>', os.environ['DJANGO_SETTINGS_MODULE'])
    print('>>>', settings.DATABASES)


    #os.environ['DJANGO_SETTINGS_MODULE'] = 'django_test_proj.settings_postgres'
    settings.configure()
'''

