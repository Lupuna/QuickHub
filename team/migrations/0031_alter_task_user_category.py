# Generated by Django 4.2.6 on 2024-02-17 17:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0030_merge_20240217_2141'),
    ]

    operations = [
        migrations.AlterField(
            model_name='task',
            name='user_category',
            field=models.ManyToManyField(related_name='tasks', through='team.Taskboard', to='team.category'),
        ),
    ]