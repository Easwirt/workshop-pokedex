# Generated by Django 5.0.4 on 2024-06-23 11:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minigame', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='boss',
            name='image',
            field=models.ImageField(upload_to='game/bosses/'),
        ),
    ]
