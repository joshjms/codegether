# Generated by Django 4.1.1 on 2022-10-22 17:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codegether', '0013_remove_project_slug'),
    ]

    operations = [
        migrations.AddField(
            model_name='project',
            name='slug',
            field=models.SlugField(null=True),
        ),
    ]
