# Generated by Django 4.1.1 on 2022-10-02 08:26

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codegether', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='project',
            name='desc',
            field=models.TextField(),
        ),
    ]
