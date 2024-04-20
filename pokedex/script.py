import sqlite3
import django
django.setup()
from pokemons.models import Pokemon


# Подключение к вашей базе данных SQLite
conn = sqlite3.connect('pokedex.sqlite')

# Создание курсора для выполнения запросов
cursor = conn.cursor()

# Выполнение запроса к базе данных SQLite
cursor.execute('SELECT * FROM pokemon')

# Получение всех результатов запроса
rows = cursor.fetchall()

# Обработка результатов и сохранение их в модели Pokemon
for row in rows:
    pokemon = Pokemon(
        abilities=row[1],
        against_bug=row[2],
        against_dark=row[3],
        against_dragon=row[4],
        against_electric=row[5],
        against_fairy=row[6],
        against_fight=row[7],
        against_fire=row[8],
        against_flying=row[9],
        against_ghost=row[10],
        against_grass=row[11],
        against_ground=row[12],
        against_ice=row[13],
        against_normal=row[14],
        against_poison=row[15],
        against_psychic=row[16],
        against_rock=row[17],
        against_steel=row[18],
        against_water=row[19],
        attack=row[20],
        base_egg_steps=row[21],
        base_happiness=row[22],
        base_total=row[23],
        capture_rate=row[24],
        classification=row[25],
        defense=row[26],
        experience_growth=row[27],
        height=row[28],
        hp=row[29],
        japanese_name=row[30],
        name=row[31],
        percentage_male=row[32],
        pokedex_number=row[33],
        sp_attack=row[34],
        sp_defense=row[35],
        speed=row[36],
        type1=row[37],
        type2=row[38],
        weight=row[39],
        generation=row[40],
        is_legendary=row[41]
    )
    pokemon.save()

conn.close()