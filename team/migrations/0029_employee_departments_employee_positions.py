# Generated by Django 4.2.6 on 2024-02-16 04:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0028_employee_companies'),
    ]

    operations = [
        migrations.AddField(
            model_name='employee',
            name='departments',
            field=models.ManyToManyField(related_name='employees', through='team.EmployeeCompany', to='team.department'),
        ),
        migrations.AddField(
            model_name='employee',
            name='positions',
            field=models.ManyToManyField(related_name='employees', through='team.EmployeeCompany', to='team.positions'),
        ),
    ]