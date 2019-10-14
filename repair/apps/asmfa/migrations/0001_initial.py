# Generated by Django 2.2.6 on 2019-10-14 15:18

import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import repair.apps.login.models.bases
import repair.apps.utils.protect_cascade


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('nace', models.CharField(max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ActivityGroup',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('done', models.BooleanField(default=False)),
                ('code', models.CharField(choices=[('P1', 'Production'), ('P2', 'Production of packaging'), ('P3', 'Packaging'), ('D', 'Distribution'), ('S', 'Selling'), ('C', 'Consuming'), ('SC', 'Selling and Consuming'), ('R', 'Return Logistics'), ('COL', 'Collection'), ('W', 'Waste Management'), ('imp', 'Import'), ('exp', 'Export')], max_length=255)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ActivityStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField(blank=True, max_length=510, null=True)),
                ('year', models.IntegerField(default=2019)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('done', models.BooleanField(default=False)),
                ('id', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='ActorStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField(blank=True, max_length=510, null=True)),
                ('year', models.IntegerField(default=2019)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Flow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route', models.BooleanField(default=False)),
                ('collector', models.BooleanField(default=False)),
                ('trips', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField(blank=True, max_length=510, null=True)),
                ('amount', models.BigIntegerField(blank=True, default=0)),
                ('year', models.IntegerField(default=2019)),
                ('waste', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='FlowChain',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('route', models.BooleanField(default=False)),
                ('collector', models.BooleanField(default=False)),
                ('trips', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField(blank=True, max_length=510, null=True)),
                ('amount', models.BigIntegerField(blank=True, default=0)),
                ('year', models.IntegerField(default=2019)),
                ('waste', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='GroupStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField(blank=True, max_length=510, null=True)),
                ('year', models.IntegerField(default=2019)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Keyflow',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('code', models.TextField(choices=[('Org', 'Organic'), ('CDW', 'Construction & Demolition'), ('Food', 'Food'), ('MSW', 'Municipal Solid Waste'), ('PCPW', 'Post-Consumer Plastic'), ('HHW', 'Household Hazardous Waste')])),
                ('name', models.TextField()),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='KeyflowInCasestudy',
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
            name='Location',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('geom', django.contrib.gis.db.models.fields.PointField(blank=True, null=True, srid=4326)),
                ('name', models.TextField(blank=True, null=True)),
                ('postcode', models.CharField(blank=True, max_length=10, null=True)),
                ('address', models.CharField(blank=True, max_length=255, null=True)),
                ('country', models.CharField(blank=True, max_length=255, null=True)),
                ('city', models.CharField(blank=True, max_length=255, null=True)),
                ('role', models.TextField(blank=True, choices=[('Producer', 'Producer'), ('Consumer', 'Consumer')], null=True)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Process',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.TextField(default='', max_length=255)),
                ('code', models.TextField(default='', max_length=255)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Waste',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('ewc_code', models.CharField(default='', max_length=255)),
                ('ewc_name', models.CharField(default='', max_length=255)),
                ('hazardous', models.BooleanField(default=False)),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='Activity2Activity',
            fields=[
                ('flow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='asmfa.Flow')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=('asmfa.flow',),
        ),
        migrations.CreateModel(
            name='Actor2Actor',
            fields=[
                ('flow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='asmfa.Flow')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=('asmfa.flow',),
        ),
        migrations.CreateModel(
            name='Group2Group',
            fields=[
                ('flow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='asmfa.Flow')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=('asmfa.flow',),
        ),
        migrations.CreateModel(
            name='Location2Location',
            fields=[
                ('flow_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='asmfa.Flow')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=('asmfa.flow',),
        ),
        migrations.CreateModel(
            name='Material',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('keyflow', models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='asmfa.KeyflowInCasestudy')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
        migrations.CreateModel(
            name='LocationStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('amount', models.IntegerField(blank=True, default=0)),
                ('description', models.TextField(blank=True, max_length=510, null=True)),
                ('year', models.IntegerField(default=2019)),
                ('keyflow', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='asmfa.KeyflowInCasestudy')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='stocks', to='asmfa.Location')),
            ],
            options={
                'abstract': False,
                'default_permissions': ('add', 'change', 'delete', 'view'),
            },
            bases=(repair.apps.login.models.bases.GDSEModelMixin, models.Model),
        ),
    ]
