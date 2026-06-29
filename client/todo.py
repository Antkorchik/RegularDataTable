import sqlite3

# Подключаемся к базе
conn = sqlite3.connect('auth.db')
cursor = conn.cursor()

# Сначала проверим существование таблицы
cursor.execute("SELECT name FROM sqlite_master WHERE type='table'")
tables = cursor.fetchall()
print("Таблицы в базе:", tables)

# Если таблицы users нет, создаем ее
if not any('users' in table for table in tables):
    print("Создаем таблицу users...")
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            user_id INTEGER PRIMARY KEY AUTOINCREMENT,
            login TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
            last_active_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    conn.commit()
    print("Таблица users создана!")

# Теперь можно выполнять запрос
cursor.execute("SELECT * FROM users")
users = cursor.fetchall()

if users:
    print("Пользователи в базе:")
    for user in users:
        print(user)
else:
    print("Таблица users пустая")

conn.close()