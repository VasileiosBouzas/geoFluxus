# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-27 19:22
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('login', '0002_auto_20171027_1908'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('source', models.BooleanField(default=False)),
                ('sink', models.BooleanField(default=False)),
                ('nace', models.CharField(max_length=255, unique=True)),
                ('name', models.CharField(max_length=255)),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Activity2Activity',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(blank=True, choices=[('PET', 'PET plastic'), ('Org', 'Organic'), ('PVC', 'PVC plastic')], max_length=255)),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('quality', models.CharField(blank=True, choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low'), ('4', 'Waste')], max_length=255)),
                ('casestudy', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Inputs', to='asmfa.Activity', to_field='nace')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Outputs', to='asmfa.Activity', to_field='nace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityGroup',
            fields=[
                ('source', models.BooleanField(default=False)),
                ('sink', models.BooleanField(default=False)),
                ('code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('P1', 'Production'), ('P2', 'Production of packaging'), ('P3', 'Packaging'), ('D', 'Distribution'), ('S', 'Selling'), ('C', 'Consuming'), ('SC', 'Selling and Cosuming'), ('R', 'Return Logistics'), ('COL', 'Collection'), ('W', 'Waste Management'), ('imp', 'Import'), ('exp', 'Export')], max_length=255)),
                ('casestudy', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(blank=True, choices=[('PET', 'PET plastic'), ('Org', 'Organic'), ('PVC', 'PVC plastic')], max_length=255)),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('quality', models.CharField(blank=True, choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low'), ('4', 'Waste')], max_length=255)),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stocks', to='asmfa.Activity', to_field='nace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('source', models.BooleanField(default=False)),
                ('sink', models.BooleanField(default=False)),
                ('BvDid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('consCode', models.CharField(max_length=255)),
                ('year', models.PositiveSmallIntegerField()),
                ('revenue', models.PositiveIntegerField()),
                ('employees', models.PositiveSmallIntegerField()),
                ('BvDii', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255)),
                ('own_activity', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Actors', to='asmfa.Activity', to_field='nace')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Actor2Actor',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(blank=True, choices=[('PET', 'PET plastic'), ('Org', 'Organic'), ('PVC', 'PVC plastic')], max_length=255)),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('quality', models.CharField(blank=True, choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low'), ('4', 'Waste')], max_length=255)),
                ('casestudy', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Inputs', to='asmfa.Actor')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Outputs', to='asmfa.Actor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActorStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(blank=True, choices=[('PET', 'PET plastic'), ('Org', 'Organic'), ('PVC', 'PVC plastic')], max_length=255)),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('quality', models.CharField(blank=True, choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low'), ('4', 'Waste')], max_length=255)),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stocks', to='asmfa.Actor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataEntry',
            fields=[
                ('user', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('source', models.CharField(max_length=255)),
            ],
        ),
        migrations.CreateModel(
            name='Geolocation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
        ),
        migrations.CreateModel(
            name='Group2Group',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(blank=True, choices=[('PET', 'PET plastic'), ('Org', 'Organic'), ('PVC', 'PVC plastic')], max_length=255)),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('quality', models.CharField(blank=True, choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low'), ('4', 'Waste')], max_length=255)),
                ('casestudy', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='login.CaseStudy')),
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Inputs', to='asmfa.ActivityGroup')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Outputs', to='asmfa.ActivityGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='GroupStock',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('material', models.CharField(blank=True, choices=[('PET', 'PET plastic'), ('Org', 'Organic'), ('PVC', 'PVC plastic')], max_length=255)),
                ('amount', models.PositiveIntegerField(blank=True)),
                ('quality', models.CharField(blank=True, choices=[('1', 'High'), ('2', 'Medium'), ('3', 'Low'), ('4', 'Waste')], max_length=255)),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stocks', to='asmfa.ActivityGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='own_activitygroup',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Activities', to='asmfa.ActivityGroup'),
        ),
    ]
