# Generated by Django 4.1 on 2023-01-04 04:11

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0019_playback_party_code'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='playback',
            name='song',
        ),
        migrations.RemoveField(
            model_name='queue',
            name='song',
        ),
        migrations.AddField(
            model_name='playback',
            name='song_tag',
            field=models.CharField(default=None, max_length=50),
            preserve_default=False,
        ),
        migrations.AddField(
            model_name='queue',
            name='song_tag',
            field=models.CharField(default='a', max_length=50),
            preserve_default=False,
        ),
    ]
