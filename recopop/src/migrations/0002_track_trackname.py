# Generated by Django 4.2.3 on 2023-07-17 20:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('src', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='track',
            name='trackName',
            field=models.CharField(default='unknowntrack', max_length=100),
        ),
    ]
