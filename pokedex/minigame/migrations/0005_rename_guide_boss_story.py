# Generated by Django 5.0.4 on 2024-06-24 11:30

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minigame', '0004_boss_defeat_text_boss_victory_text'),
    ]

    operations = [
        migrations.RenameField(
            model_name='boss',
            old_name='guide',
            new_name='story',
        ),
    ]