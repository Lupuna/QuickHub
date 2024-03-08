# Generated by Django 4.2.6 on 2024-02-04 08:23

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0016_alter_positions_title'),
    ]

    operations = [
        migrations.AlterUniqueTogether(
            name='department',
            unique_together={('company_id', 'title')},
        ),
        migrations.AlterUniqueTogether(
            name='positions',
            unique_together={('company_id', 'title')},
        ),
    ]
