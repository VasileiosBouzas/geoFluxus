# Generated by Django 2.0 on 2018-10-04 09:44

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('statusquo', '0009_auto_20180927_1809'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='target',
            name='aim',
        ),
        migrations.RemoveField(
            model_name='target',
            name='impact_category',
        ),
        migrations.RemoveField(
            model_name='target',
            name='spatial_reference',
        ),
        migrations.RemoveField(
            model_name='target',
            name='target_value',
        ),
        migrations.RemoveField(
            model_name='target',
            name='user',
        ),
        migrations.AddField(
            model_name='userobjective',
            name='target_areas',
            field=models.ManyToManyField(to='statusquo.AreaOfProtection'),
        ),
        migrations.AlterField(
            model_name='flowtarget',
            name='userobjective',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='flow_targets', to='statusquo.UserObjective'),
        ),
        migrations.DeleteModel(
            name='Target',
        ),
    ]
