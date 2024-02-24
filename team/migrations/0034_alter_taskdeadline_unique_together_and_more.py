# Generated by Django 4.2.6 on 2024-02-24 16:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0033_taskdeadline_userdeadline_delete_userprojecttime_and_more'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='taskdeadline',
            unique_together=set(),
        ),
        migrations.AlterField(
            model_name='taskdeadline',
            name='time_start',
            field=models.DateTimeField(blank=True),
        ),
        migrations.RemoveField(
            model_name='taskdeadline',
            name='user_deadline_id',
        ),
    ]
