# Generated by Django 5.0.4 on 2024-06-24 17:51

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minigame', '0007_fight_clicks_fight_health_fight_time'),
    ]

    operations = [
        migrations.RenameField(
            model_name='fight',
            old_name='user',
            new_name='profile',
        ),
    ]
