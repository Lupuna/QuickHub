# Generated by Django 4.2.6 on 2024-02-26 07:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0034_remove_task_status_project_task_status'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='satus',
            field=models.CharField(default='Work', max_length=40),
        ),
    ]
