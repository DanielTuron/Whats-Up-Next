# Generated by Django 4.1 on 2023-01-02 21:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0003_user_rename_createdat_party_created_at'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='user',
            name='room_code',
        ),
        migrations.AddField(
            model_name='user',
            name='party',
            field=models.ForeignKey(default=None, on_delete=django.db.models.deletion.CASCADE, to='api.party'),
            preserve_default=False,
        ),
    ]
