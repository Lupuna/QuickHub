# Generated by Django 4.2.6 on 2024-02-29 14:00

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0038_remove_task_status_alter_employeecompany_company_id_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='task_status',
            field=models.CharField(default=1, max_length=40),
            preserve_default=False,
        ),
    ]
