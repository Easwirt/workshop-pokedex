# Generated by Django 5.0.4 on 2024-06-24 15:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minigame', '0006_fight'),
    ]

    operations = [
        migrations.AddField(
            model_name='fight',
            name='clicks',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='fight',
            name='health',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='fight',
            name='time',
            field=models.IntegerField(default=0),
        ),
    ]
