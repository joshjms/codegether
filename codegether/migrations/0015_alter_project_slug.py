# Generated by Django 4.1.1 on 2022-10-22 17:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codegether', '0014_project_slug'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='slug',
            field=models.SlugField(default=0, unique=True),
            preserve_default=False,
        ),
    ]