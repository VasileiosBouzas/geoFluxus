# Generated by Django 2.2.6 on 2019-10-30 18:20

from django.db import migrations
import enumfields.fields
import repair.apps.statusquo.models.filters


class Migration(migrations.Migration):

    dependencies = [
        ('statusquo', '0008_auto_20191030_1815'),
    ]

    operations = [
        migrations.AddField(
            model_name='flowfilter',
            name='year',
            field=enumfields.fields.EnumIntegerField(default=1, enum=repair.apps.statusquo.models.filters.Year),
        ),
    ]
