# Generated by Django 2.2.6 on 2019-10-14 15:18

import django.contrib.gis.db.models.fields
import django.core.validators
from django.db import migrations, models
import enumfields.fields
import re
import repair.apps.changes.models.solutions
import repair.apps.login.models.bases


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='AffectedFlow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FlowReference',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('include_child_materials', models.BooleanField(default=False)),
                ('waste', models.IntegerField(default=-1)),
                ('hazardous', models.IntegerField(default=-1)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ImplementationArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(blank=True, null=True, srid=4326)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ImplementationQuantity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('value', models.FloatField()),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ImplementationQuestion',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question', models.TextField(default='')),
                ('unit', models.CharField(blank=True, default='', max_length=100)),
                ('select_values', models.TextField(blank=True, validators=[django.core.validators.RegexValidator(re.compile('^([-+]?\\d*\\.?\\d+[,\\s]*)+$'), 'Enter only floats separated by commas.', 'invalid')])),
                ('step', models.FloatField(null=True)),
                ('min_value', models.FloatField(default=0)),
                ('max_value', models.FloatField(default=1)),
                ('is_absolute', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='PossibleImplementationArea',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.MultiPolygonField(srid=4326)),
                ('question', models.TextField(default='')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Solution',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('description', models.TextField(default='')),
                ('documentation', models.TextField(default='')),
                ('currentstate_image', models.ImageField(blank=True, null=True, upload_to='charts')),
                ('effect_image', models.ImageField(blank=True, null=True, upload_to='charts')),
                ('activities_image', models.ImageField(blank=True, null=True, upload_to='charts')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SolutionCategory',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SolutionInStrategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('note', models.TextField(blank=True, null=True)),
                ('priority', models.IntegerField(default=0)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='SolutionPart',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('documentation', models.TextField(default='')),
                ('scheme', enumfields.fields.EnumIntegerField(default=0, enum=repair.apps.changes.models.solutions.Scheme)),
                ('priority', models.IntegerField(default=0)),
                ('is_absolute', models.BooleanField(default=False)),
                ('a', models.FloatField()),
                ('b', models.FloatField()),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Strategy',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField()),
                ('status', models.IntegerField(default=0)),
                ('date', models.DateTimeField(null=True)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
    ]
