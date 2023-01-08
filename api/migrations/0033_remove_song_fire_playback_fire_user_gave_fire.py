# Generated by Django 4.1 on 2023-01-07 05:35

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0032_song_fire'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='song',
            name='fire',
        ),
        migrations.AddField(
            model_name='playback',
            name='fire',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='user',
            name='gave_fire',
            field=models.BooleanField(default=False),
        ),
    ]