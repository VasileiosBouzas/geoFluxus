# Generated by Django 2.0 on 2018-10-18 13:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyarea', '0026_auto_20180831_1441'),
    ]

    operations = [
        migrations.AddField(
            model_name='stakeholder',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
