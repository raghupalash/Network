# Generated by Django 3.1.2 on 2020-11-15 06:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0004_user_following'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_following',
            old_name='following_user_id',
            new_name='following_user',
        ),
        migrations.RenameField(
            model_name='user_following',
            old_name='user_id',
            new_name='user',
        ),
    ]
