# Generated by Django 4.1.1 on 2022-10-22 17:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codegether', '0010_alter_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(blank=True, default='built-in-function-id'),
        ),
    ]
