# Generated by Django 5.0.4 on 2024-06-25 10:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('pokemons', '0004_pokemon_price'),
    ]

    operations = [
        migrations.AlterField(
            model_name='pokemon',
            name='attack',
            field=models.IntegerField(default=0),
        ),
    ]
