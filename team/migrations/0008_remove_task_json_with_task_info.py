# Generated by Django 4.2.6 on 2023-11-26 07:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0007_remove_task_file_remove_task_image_taskimage_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='task',
            name='json_with_task_info',
        ),
    ]
