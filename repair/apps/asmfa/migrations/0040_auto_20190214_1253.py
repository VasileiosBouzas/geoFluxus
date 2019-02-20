# Generated by Django 2.0 on 2019-02-14 11:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0039_fractionflow'),
    ]

    operations = [
        migrations.AlterField(
            model_name='activity2activity',
            name='amount',
            field=models.BigIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='actor2actor',
            name='amount',
            field=models.BigIntegerField(blank=True, default=0),
        ),
        migrations.AlterField(
            model_name='group2group',
            name='amount',
            field=models.BigIntegerField(blank=True, default=0),
        ),
    ]