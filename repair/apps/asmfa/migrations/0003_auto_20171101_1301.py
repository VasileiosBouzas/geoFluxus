# -*- coding: utf-8 -*-
# Generated by Django 1.11.6 on 2017-11-01 12:01
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0002_auto_20171101_1253'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='activity',
            name='own_activitygroup',
        ),
        migrations.RemoveField(
            model_name='actor2actor',
            name='destination2',
        ),
        migrations.RemoveField(
            model_name='actor2actor',
            name='origin2',
        ),
        migrations.RemoveField(
            model_name='actorstock',
            name='origin2',
        ),
        migrations.RemoveField(
            model_name='group2group',
            name='destination2',
        ),
        migrations.RemoveField(
            model_name='group2group',
            name='origin2',
        ),
        migrations.RemoveField(
            model_name='groupstock',
            name='origin2',
        ),
    ]