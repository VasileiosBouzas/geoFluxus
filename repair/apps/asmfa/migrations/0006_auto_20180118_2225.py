# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2018-01-18 21:25
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0005_publicationincasestudy'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='publicationincasestudy',
            name='casestudy',
        ),
        migrations.RemoveField(
            model_name='publicationincasestudy',
            name='publication',
        ),
        migrations.DeleteModel(
            name='PublicationInCasestudy',
        ),
    ]
