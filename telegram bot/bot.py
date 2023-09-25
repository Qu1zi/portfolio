import sqlite3
import telebot

# Создаем экземпляр бота с указанием токена
bot = telebot.TeleBot('6263732751:AAGA_EGitqoN4GL7U7U_uhsE9_nv0o3YXAk')

# Функция-обработчик команды /start
@bot.message_handler(commands=['start'])
def start(message):
    commands = [
        "/add <Имя> <Фамилия> <населенный пункт> <адрес> - Добавить информацию о прописке",
        "/get <Имя> <Фамилия> - Получить информацию о прописке",
        "/all - Показать все загруженные прописки",
        "/delete <Имя> <Фамилия> - Удалить информацию о прописке"
    ]
    commands_text = "\n".join(commands)
    bot.send_message(message.chat.id, f"Привет! Я бот для информации о прописке.\n\nДоступные команды:\n{commands_text}")

# Функция-обработчик команды /add
@bot.message_handler(commands=['add'])
def add_propiska(message):
    # Получаем параметры команды
    params = message.text.split(maxsplit=4)[1:]
    if len(params) != 4:
        bot.send_message(message.chat.id, "Используйте команду /add <Имя> <Фамилия> <населенный пункт> <адрес>")
        return

    name = params[0]
    surname = params[1]
    settlement = params[2]
    address = params[3]

    # Проверяем, существует ли прописка уже в базе данных
    conn = sqlite3.connect('propiska.db')
    c = conn.cursor()
    c.execute("SELECT * FROM propiska WHERE name = ? AND surname = ? AND settlement = ? AND address = ?", (name, surname, settlement, address))
    existing_propiska = c.fetchone()
    if existing_propiska:
        bot.send_message(message.chat.id, "Данная прописка уже существует.")
    else:
        # Сохраняем информацию в базе данных
        c.execute("INSERT INTO propiska (name, surname, settlement, address) VALUES (?, ?, ?, ?)", (name, surname, settlement, address))
        conn.commit()
        bot.send_message(message.chat.id, "Информация о прописке добавлена.")
    conn.close()

# Функция-обработчик команды /get
@bot.message_handler(commands=['get'])
def get_propiska(message):
    # Получаем параметры команды
    params = message.text.split()[1:]
    if len(params) != 2:
        bot.send_message(message.chat.id, "Используйте команду /get <Имя> <Фамилия>")
        return

    name = params[0]
    surname = params[1]

    # Ищем информацию о прописке в базе данных
    conn = sqlite3.connect('propiska.db')
    c = conn.cursor()
    c.execute("SELECT settlement, address FROM propiska WHERE name = ? AND surname = ?", (name, surname))
    result = c.fetchone()
    conn.close()

    if result:
        settlement, address = result
        bot.send_message(message.chat.id, f"Информация о прописке:\nИмя: {name}\nФамилия: {surname}\nНаселенный пункт: {settlement}\nАдрес: {address}")
    else:
        bot.send_message(message.chat.id, f"Информация о прописке для {name} {surname} не найдена.")

# Функция-обработчик команды /all
@bot.message_handler(commands=['all'])
def all_propiski(message):
    # Получаем все прописки из базы данных
    conn = sqlite3.connect('propiska.db')
    c = conn.cursor()
    c.execute("SELECT name, surname, settlement, address FROM propiska")
    results = c.fetchall()
    conn.close()

    if results:
        propiski = []
        for result in results:
            name, surname, settlement, address = result
            propiska_info = f"Имя: {name}\nФамилия: {surname}\nНаселенный пункт: {settlement}\nАдрес: {address}"
            propiski.append(propiska_info)

        all_propiski_text = "\n\n".join(propiski)
        bot.send_message(message.chat.id, f"Все загруженные прописки:\n\n{all_propiski_text}")
    else:
        bot.send_message(message.chat.id, "Нет загруженных прописок.")

# Функция-обработчик команды /delete
@bot.message_handler(commands=['delete'])
def delete_propiska(message):
    # Получаем параметры команды
    params = message.text.split()[1:]
    if len(params) != 2:
        bot.send_message(message.chat.id, "Используйте команду /delete <Имя> <Фамилия>")
        return

    name = params[0]
    surname = params[1]

    # Удаляем прописку из базы данных
    conn = sqlite3.connect('propiska.db')
    c = conn.cursor()
    c.execute("DELETE FROM propiska WHERE name = ? AND surname = ?", (name, surname))
    conn.commit()
    conn.close()

    bot.send_message(message.chat.id, f"Прописка для {name} {surname} удалена.")

# Главный цикл бота
bot.polling()
