import sqlite3

# Создаем подключение к базе данных
conn = sqlite3.connect('propiska.db')
c = conn.cursor()

# Создаем таблицу "propiska"
c.execute('''
    CREATE TABLE IF NOT EXISTS propiska (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT NOT NULL,
        surname TEXT NOT NULL,
        settlement TEXT NOT NULL,
        address TEXT NOT NULL
    )
''')

# Сохраняем изменения и закрываем соединение
conn.commit()
conn.close()
