# Generated by Django 4.1 on 2023-01-02 21:08

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0009_alter_user_party'),
    ]

    operations = [
        migrations.AlterField(
            model_name='user',
            name='party',
            field=models.ForeignKey(blank=True, default=1, null=True, on_delete=django.db.models.deletion.CASCADE, to='api.party'),
        ),
    ]
