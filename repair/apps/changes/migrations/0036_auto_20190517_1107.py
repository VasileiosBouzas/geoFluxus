# Generated by Django 2.2.1 on 2019-05-17 11:07

from django.db import migrations, models
import repair.apps.utils.protect_cascade


class Migration(migrations.Migration):

    dependencies = [
        ('asmfa', '0042_auto_20190409_0925'),
        ('changes', '0035_auto_20190516_1042'),
    ]

    operations = [
        migrations.AddField(
            model_name='solutionpart',
            name='implemenentation_flow_solution_part',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='implementation_part', to='changes.SolutionPart'),
        ),
        migrations.AddField(
            model_name='solutionpart',
            name='new_material',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='asmfa.Material'),
        ),
        migrations.AlterField(
            model_name='solutionpart',
            name='implementation_flow_material',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='implementation_material', to='asmfa.Material'),
        ),
        migrations.AlterField(
            model_name='solutionpart',
            name='implementation_flow_origin_activity',
            field=models.ForeignKey(null=True, on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, related_name='implementation_origin', to='asmfa.Activity'),
        ),
    ]
