# Generated by Django 4.2.6 on 2024-02-17 17:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0031_alter_task_user_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]