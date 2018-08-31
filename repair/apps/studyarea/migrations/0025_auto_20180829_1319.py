# Generated by Django 2.0 on 2018-08-29 11:19

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0029_auto_20180503_1411'),
        ('studyarea', '0024_update_parent_area'),
    ]

    operations = [
        migrations.DeleteModel(
            name='CityBlock',
        ),
        migrations.DeleteModel(
            name='CityDistrict',
        ),
        migrations.DeleteModel(
            name='CityNeighbourhood',
        ),
        migrations.DeleteModel(
            name='Continent',
        ),
        migrations.DeleteModel(
            name='Country',
        ),
        migrations.DeleteModel(
            name='District',
        ),
        migrations.DeleteModel(
            name='House',
        ),
        migrations.DeleteModel(
            name='Municipality',
        ),
        migrations.DeleteModel(
            name='NUTS1',
        ),
        migrations.DeleteModel(
            name='NUTS2',
        ),
        migrations.DeleteModel(
            name='NUTS3',
        ),
        migrations.DeleteModel(
            name='StreetSection',
        ),
        migrations.DeleteModel(
            name='World',
        ),
    ]