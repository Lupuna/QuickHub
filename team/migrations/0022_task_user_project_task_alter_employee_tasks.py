# Generated by Django 4.2.6 on 2024-02-13 12:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0021_alter_userproject_unique_together'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='user_project_task',
            field=models.ManyToManyField(through='team.UserProjectTask', to='team.userproject'),
        ),
        migrations.AlterField(
            model_name='employee',
            name='tasks',
            field=models.ManyToManyField(blank=True, related_name='executors', to='team.task'),
        ),
    ]