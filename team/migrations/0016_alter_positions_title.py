# Generated by Django 4.2.6 on 2024-02-04 08:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0015_alter_positions_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='positions',
            name='title',
            field=models.CharField(max_length=40),
        ),
    ]
