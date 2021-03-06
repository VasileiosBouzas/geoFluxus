# Generated by Django 2.0 on 2018-04-26 17:51

from django.db import migrations, models
import repair.apps.utils.protect_cascade


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0011_auto_20180426_1841'),
    ]

    operations = [
        migrations.AlterField(
            model_name='solutioninimplementation',
            name='implementation',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='changes.Implementation'),
        ),
        migrations.AlterField(
            model_name='solutioninimplementation',
            name='solution',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='changes.Solution'),
        ),
        migrations.AlterField(
            model_name='solutionquantity',
            name='unit',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='changes.Unit'),
        ),
        migrations.AlterField(
            model_name='solutionratiooneunit',
            name='unit',
            field=models.ForeignKey(on_delete=repair.apps.utils.protect_cascade.PROTECT_CASCADE, to='changes.Unit'),
        ),
    ]
