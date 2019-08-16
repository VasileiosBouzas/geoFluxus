# Generated by Django 2.2.1 on 2019-07-01 09:36

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('changes', '0039_auto_20190524_1108'),
    ]

    operations = [
        migrations.AlterField(
            model_name='implementationquantity',
            name='question',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='implementation_question', to='changes.ImplementationQuestion'),
        ),
        migrations.AlterField(
            model_name='solutionpart',
            name='solution',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='solution_parts', to='changes.Solution'),
        ),
    ]