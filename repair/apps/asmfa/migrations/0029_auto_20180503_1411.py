# Generated by Django 2.0 on 2018-05-03 12:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0028_auto_20180502_1427'),
    ]

    operations = [
        migrations.AlterField(
            model_name='administrativelocation',
            name='country',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
        migrations.AlterField(
            model_name='operationallocation',
            name='country',
            field=models.CharField(blank=True, default='', max_length=255),
        ),
    ]