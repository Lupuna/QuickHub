# Generated by Django 4.2.6 on 2024-02-27 13:18

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0037_merge_20240227_2018'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='status',
        ),
        migrations.AlterField(
            model_name='employeecompany',
            name='company_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='company', to='team.company'),
        ),
        migrations.AlterField(
            model_name='employeecompany',
            name='department_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='department', to='team.department'),
        ),
        migrations.AlterField(
            model_name='employeecompany',
            name='employee_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='employee', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='employeecompany',
            name='position_id',
            field=models.ForeignKey(blank=True, null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='position', to='team.positions'),
        ),
    ]