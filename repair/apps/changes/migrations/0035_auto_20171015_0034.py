# -*- coding: utf-8 -*-
# Generated by Django 1.11.5 on 2017-10-14 22:34
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0034_auto_20171008_2111'),
    ]

    operations = [
        migrations.CreateModel(
            name='Activity',
            fields=[
                ('nace', models.CharField(max_length=255, primary_key=True, serialize=False)),
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
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Inputs', to='changes.Activity')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Outputs', to='changes.Activity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='ActivityGroup',
            fields=[
                ('code', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(choices=[('P1', 'Production'), ('P2', 'Production of packaging'), ('P3', 'Packaging'), ('D', 'Distribution'), ('S', 'Selling'), ('C', 'Consuming'), ('SC', 'Selling and Cosuming'), ('R', 'Return Logistics'), ('COL', 'Collection'), ('W', 'Waste Management'), ('imp', 'Import'), ('exp', 'Export')], max_length=255)),
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
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stocks', to='changes.Activity')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='Actor',
            fields=[
                ('BvDid', models.CharField(max_length=255, primary_key=True, serialize=False)),
                ('name', models.CharField(max_length=255)),
                ('consCode', models.CharField(max_length=255)),
                ('year', models.PositiveSmallIntegerField()),
                ('revenue', models.PositiveIntegerField()),
                ('employees', models.PositiveSmallIntegerField()),
                ('BvDii', models.CharField(max_length=255)),
                ('website', models.CharField(max_length=255)),
                ('own_activity', models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Actors', to='changes.Activity')),
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
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Inputs', to='changes.Actor')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Outputs', to='changes.Actor')),
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
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stocks', to='changes.Actor')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='DataEntry',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
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
                ('destination', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Inputs', to='changes.ActivityGroup')),
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Outputs', to='changes.ActivityGroup')),
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
                ('origin', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='Stocks', to='changes.ActivityGroup')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.AddField(
            model_name='activity',
            name='own_activitygroup',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, related_name='Activities', to='changes.ActivityGroup'),
        ),
    ]