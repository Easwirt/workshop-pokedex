# Generated by Django 5.0.4 on 2024-04-20 14:47

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0005_profile_coints'),
    ]

    operations = [
        migrations.RenameField(
            model_name='profile',
            old_name='coints',
            new_name='coins',
        ),
    ]