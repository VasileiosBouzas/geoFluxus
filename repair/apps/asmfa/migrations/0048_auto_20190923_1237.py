# Generated by Django 2.2.4 on 2019-09-23 12:37

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0046_auto_20190830_1048'),
        ('asmfa', '0047_auto_20190902_1402'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='strategyfractionflow',
            unique_together={('strategy', 'fractionflow')},
        ),
    ]
