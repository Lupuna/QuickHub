# Generated by Django 4.2.6 on 2024-02-15 10:58

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0024_rename_user_project_id_taskboard_category_id'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='user_project_task',
        ),
        migrations.AddField(
            model_name='task',
            name='user_category',
            field=models.ManyToManyField(related_name='category_tasks', through='team.Taskboard', to='team.category'),
        ),
    ]