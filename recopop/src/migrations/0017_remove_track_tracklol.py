# Generated by Django 4.2.3 on 2023-07-21 01:17

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0016_remove_post_user_obj_id_track_tracklol_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='track',
            name='trackLol',
        ),
    ]
