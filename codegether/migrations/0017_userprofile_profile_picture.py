# Generated by Django 4.1.1 on 2022-10-23 04:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('codegether', '0016_remove_userprofile_email_remove_userprofile_username_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='userprofile',
            name='profile_picture',
            field=models.ImageField(default=0, upload_to='pfp'),
            preserve_default=False,
        ),
    ]
