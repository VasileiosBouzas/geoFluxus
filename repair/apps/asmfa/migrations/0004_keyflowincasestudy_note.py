# Generated by Django 2.2.6 on 2019-10-17 14:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0003_auto_20191015_1416'),
    ]

    operations = [
        migrations.AddField(
            model_name='keyflowincasestudy',
            name='note',
            field=models.TextField(blank=True, default=''),
        ),
    ]