# Generated by Django 4.2.6 on 2024-01-08 09:48

from django.db import migrations, models
import team.utils


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0007_linksresources_title'),
    ]

    operations = [
        migrations.AlterField(
            model_name='employee',
            name='json_with_settings_info',
            field=models.JSONField(blank=True, default=team.utils.create_base_settings_json_to_employee),
        ),
    ]
