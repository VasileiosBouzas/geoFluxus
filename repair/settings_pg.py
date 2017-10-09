"""
Django settings for repair project.

Generated by 'django-admin startproject' using Django 1.11.5.

For more information on this file, see
https://docs.djangoproject.com/en/1.11/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.11/ref/settings/
"""

from repair.settings import *

DB_NAME = os.environ['DB_NAME']
DB_USER = os.environ['DB_USER']
DB_PASS = os.environ['DB_PASS']

#GDAL_LIBRARY_PATH = r'C:\OSGeo4W64\bin\gdal201.dll'

DATABASES = {
    'default': {

        #'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'ENGINE': 'django.db.backends.postgresql_psycopg2',
        'NAME': DB_NAME,
        'USER': DB_USER,
        'PASSWORD': DB_PASS,
        'HOST': 'h2020repair.bk.tudelft.nl',
        'PORT': '5432',
        'OPTIONS': {
            'sslmode': 'require',
            },
    },
}

