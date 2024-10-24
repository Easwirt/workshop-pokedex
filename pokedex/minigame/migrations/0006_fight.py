# Generated by Django 5.0.4 on 2024-06-24 15:12

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('minigame', '0005_rename_guide_boss_story'),
        ('profiles', '0008_profile_boss'),
    ]

    operations = [
        migrations.CreateModel(
            name='Fight',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('section', models.IntegerField(default=1)),
                ('status', models.IntegerField(default=1)),
                ('boss', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='minigame.boss')),
                ('user', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='profiles.profile')),
            ],
        ),
    ]
