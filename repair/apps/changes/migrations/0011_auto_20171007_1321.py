# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 11:21
from __future__ import unicode_literals

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0010_auto_20171007_1318'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='solutioninimplementation',
            name='geometries',
        ),
        migrations.RemoveField(
            model_name='solutioninimplementation',
            name='implementation',
        ),
        migrations.RemoveField(
            model_name='solutioninimplementation',
            name='notes',
        ),
        migrations.RemoveField(
            model_name='solutioninimplementation',
            name='quantities',
        ),
        migrations.RemoveField(
            model_name='solutioninimplementation',
            name='solution',
        ),
        migrations.DeleteModel(
            name='SolutionInImplementation',
        ),
    ]