# Generated by Django 4.1.1 on 2022-10-22 17:32

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('codegether', '0012_alter_project_slug'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='project',
            name='slug',
        ),
    ]