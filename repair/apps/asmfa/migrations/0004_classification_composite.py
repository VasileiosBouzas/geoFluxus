# Generated by Django 2.2.7 on 2019-12-05 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0003_auto_20191204_1609'),
    ]

    operations = [
        migrations.AddField(
            model_name='classification',
            name='composite',
            field=models.BooleanField(null=True),
        ),
    ]