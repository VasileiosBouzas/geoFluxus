# Generated by Django 2.0 on 2018-03-09 13:45

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('studyarea', '0016_auto_20180305_1311'),
    ]

    operations = [
        migrations.AddField(
            model_name='layer',
            name='z_index',
            field=models.IntegerField(default=1),
        ),
    ]