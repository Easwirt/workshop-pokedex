# Generated by Django 5.0.4 on 2024-06-13 21:19

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('profiles', '0005_alter_profile_bio'),
    ]

    operations = [
        migrations.AlterField(
            model_name='profile',
            name='bio',
            field=models.TextField(default='Hi, there!', max_length=100),
        ),
    ]
