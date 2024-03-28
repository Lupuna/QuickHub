# Generated by Django 4.2.6 on 2024-03-19 07:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0045_delete_taskdeadline'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('user_project', '0002_alter_taskboard_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='employee_id',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='categories', to=settings.AUTH_USER_MODEL, verbose_name='Работники'),
        ),
        migrations.AlterField(
            model_name='category',
            name='project_personal_notes',
            field=models.TextField(blank=True, null=True, verbose_name='Заметки'),
        ),
        migrations.AlterField(
            model_name='category',
            name='tasks',
            field=models.ManyToManyField(related_name='user_category', through='user_project.Taskboard', to='team.task', verbose_name='Задачи'),
        ),
        migrations.AlterField(
            model_name='category',
            name='title',
            field=models.CharField(max_length=40, verbose_name='Название'),
        ),
        migrations.AlterField(
            model_name='taskboard',
            name='category_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='taskboards', to='user_project.category', verbose_name='Категория'),
        ),
        migrations.AlterField(
            model_name='taskboard',
            name='json_with_subtask_and_subtask_personal_note',
            field=models.JSONField(blank=True, default=dict, verbose_name='Подзадачи'),
        ),
        migrations.AlterField(
            model_name='taskboard',
            name='task_id',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='team.task', verbose_name='Задачи'),
        ),
        migrations.AlterField(
            model_name='taskboard',
            name='task_personal_notes',
            field=models.JSONField(blank=True, default=dict, verbose_name='Заметки'),
        ),
        migrations.AlterField(
            model_name='taskboard',
            name='title',
            field=models.CharField(max_length=40, verbose_name='Категория'),
        ),
    ]