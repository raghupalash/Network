# Generated by Django 3.1.2 on 2020-11-25 04:42

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('network', '0008_post_likes'),
    ]

    operations = [
        migrations.RenameField(
            model_name='post',
            old_name='timestamp',
            new_name='timestamp_modified',
        ),
        migrations.AddField(
            model_name='post',
            name='timestamp_created',
            field=models.DateTimeField(auto_now_add=True, default=django.utils.timezone.now),
            preserve_default=False,
        ),
    ]
