# Generated by Django 2.0 on 2018-05-09 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0010_auto_20180509_1203'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casestudy',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'setupmode', 'dataentry')},
        ),
    ]
