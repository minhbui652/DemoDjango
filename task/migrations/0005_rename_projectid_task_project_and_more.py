# Generated by Django 5.0.14 on 2025-04-08 07:17

from django.db import migrations


class Migration(migrations.Migration):
    dependencies = [
        ('task', '0004_alter_project_table_alter_task_table'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='projectId',
            new_name='project',
        ),
        migrations.RenameField(
            model_name='task',
            old_name='userId',
            new_name='user',
        ),
    ]
