# Generated by Django 4.2.6 on 2023-11-29 05:35

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('team', '0008_remove_task_json_with_task_info'),
    ]

    operations = [
        migrations.AlterOrderWithRespectTo(
            name='linksresources',
            order_with_respect_to='employee_id',
        ),
        migrations.AlterOrderWithRespectTo(
            name='taskfile',
            order_with_respect_to='task_id',
        ),
        migrations.AlterOrderWithRespectTo(
            name='taskimage',
            order_with_respect_to='task_id',
        ),
    ]
