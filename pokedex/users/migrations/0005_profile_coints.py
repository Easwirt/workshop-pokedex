# Generated by Django 5.0.4 on 2024-04-20 14:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_profile_avatar'),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='coints',
            field=models.IntegerField(default=0),
        ),
    ]
