import sqlite3
import random

# Подключение к базе данных SQLite
conn = sqlite3.connect('db.sqlite3')
cursor = conn.cursor()

try:
    # Выбираем всех покемонов из таблицы
    cursor.execute('SELECT id FROM pokemons_pokemon')
    pokemon_ids = cursor.fetchall()

    for pokemon_id in pokemon_ids:
        # Генерируем случайную цену для покемона
        random_price = random.randint(100, 1000)  # Здесь можно настроить диапазон цен по вашему желанию

        cursor.execute('UPDATE pokemons_pokemon SET price = ? WHERE id = ?', (random_price, pokemon_id[0]))

    # Фиксируем изменения в базе данных
    conn.commit()
    print("Случайные цены успешно установлены для всех покемонов.")

except sqlite3.Error as e:
    print("Ошибка при работе с базой данных SQLite:", e)

finally:
    # Закрываем соединение с базой данных
    conn.close()