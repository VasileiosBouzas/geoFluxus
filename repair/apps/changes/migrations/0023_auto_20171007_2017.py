# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-07 18:17
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0022_solutioninimplementation_participants'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='userap12',
            name='case_study',
        ),
        migrations.AlterField(
            model_name='solution',
            name='user_ap12',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='changes.UserAP34'),
        ),
        migrations.AlterField(
            model_name='solutioncategory',
            name='user_ap12',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='changes.UserAP34'),
        ),
        migrations.DeleteModel(
            name='UserAP12',
        ),
    ]