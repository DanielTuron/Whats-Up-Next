# Generated by Django 4.1 on 2023-01-04 04:20

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0020_remove_playback_song_remove_queue_song_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='song',
            name='party',
            field=models.ForeignKey(default=1, on_delete=django.db.models.deletion.CASCADE, to='api.party'),
            preserve_default=False,
        ),
    ]
