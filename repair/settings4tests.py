"""
Django settings for repair project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from repair.settings import *


DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.spatialite',
        'NAME': 'db_tests.sqlite3',
    },

}

MIGRATION_MODULES = {
    'auth': None,
    'contenttypes': None,
    'default': None,
    'sessions': None,

    'changes': None,
    'login': None,
    'studyarea': None,
    'asmfa': None,
    'profiles': None,
    'snippets': None,
    'scaffold_templates': None,
}