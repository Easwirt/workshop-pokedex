# Generated by Django 5.0.4 on 2024-06-11 11:30

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0003_profile_friends'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.AddField(
            model_name='profile',
            name='friends_request',
            field=models.ManyToManyField(blank=True, related_name='friends_request', to=settings.AUTH_USER_MODEL),
        ),
    ]
