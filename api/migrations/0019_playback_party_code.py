# Generated by Django 4.1 on 2023-01-04 04:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0018_queue'),
    ]

    operations = [
        migrations.AddField(
            model_name='playback',
            name='party_code',
            field=models.CharField(default=None, max_length=4),
            preserve_default=False,
        ),
    ]