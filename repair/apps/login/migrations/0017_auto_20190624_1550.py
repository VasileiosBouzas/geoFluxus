# Generated by Django 2.2.1 on 2019-06-24 15:50

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('login', '0016_auto_20190123_1724'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='casestudy',
            options={'default_permissions': ('add', 'change', 'delete', 'view', 'setupmode', 'dataentry', 'conclusions')},
        ),
    ]