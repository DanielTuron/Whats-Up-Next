# Generated by Django 4.1 on 2023-01-04 15:56

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0026_alter_playback'),
    ]

    operations = [
        migrations.AddField(
            model_name='queue',
            name='username',
            field=models.CharField(default='aaaa', max_length=20),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='queue',
            name='user',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='api.user'),
        ),
    ]
