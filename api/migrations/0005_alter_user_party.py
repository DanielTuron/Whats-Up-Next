# Generated by Django 4.1 on 2023-01-02 21:01

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0004_remove_user_room_code_user_party'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='party',
            field=models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, to='api.party'),
        ),
    ]
