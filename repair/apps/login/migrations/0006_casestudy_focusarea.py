# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-12-18 18:34
from __future__ import unicode_literals

import django.contrib.gis.db.models.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0005_casestudy_geom'),
    ]

    operations = [
        migrations.AddField(
            model_name='casestudy',
            name='focusarea',
            field=django.contrib.gis.db.models.fields.MultiPolygonField(null=True, blank=True, srid=4326),
        ),
    ]
