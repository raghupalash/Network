# Generated by Django 3.1.2 on 2020-11-15 06:15

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0005_auto_20201115_1136'),
    ]

    operations = [
        migrations.RenameField(
            model_name='user_following',
            old_name='following_user',
            new_name='following_person',
        ),
        migrations.RenameField(
            model_name='user_following',
            old_name='user',
            new_name='person',
        ),
    ]
