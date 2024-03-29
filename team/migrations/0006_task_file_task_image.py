# Generated by Django 4.2.6 on 2023-11-26 05:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0005_subtasks_text_task_text'),
    ]

    operations = [
        migrations.AddField(
            model_name='task',
            name='file',
            field=models.FileField(blank=True, null=True, upload_to='files/%Y/%m/%d'),
        ),
        migrations.AddField(
            model_name='task',
            name='image',
            field=models.ImageField(blank=True, null=True, upload_to='images/%Y/%m/%d'),
        ),
    ]
