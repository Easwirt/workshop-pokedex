# Generated by Django 5.0.4 on 2024-06-24 18:57

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('minigame', '0009_alter_fight_options_alter_fight_boss'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='fight',
            name='section',
        ),
    ]