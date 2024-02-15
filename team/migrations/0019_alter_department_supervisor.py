# Generated by Django 4.2.6 on 2024-02-04 11:33

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0018_alter_employeecompany_unique_together'),
    ]

    operations = [
        migrations.AlterField(
            model_name='department',
            name='supervisor',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL),
        ),
    ]
