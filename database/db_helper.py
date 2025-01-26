import os
import sqlite3
import random

# Определяем путь к базе данных
DB_PATH = os.path.join(os.path.dirname(__file__), "bars.db")

def init_db():
    """Создаёт базу данных, если её ещё нет"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS bars (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        name TEXT UNIQUE NOT NULL,
        description TEXT,
        visited BOOLEAN DEFAULT 0,
        last_visit_date TEXT
    )
    """)
    conn.commit()
    conn.close()

def save_bar(data, last_visit_date):
    """Сохраняет информацию о баре в базу данных"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    INSERT INTO bars (name, description, visited, last_visit_date)
    VALUES (?, ?, ?, ?)
    """, (data["name"], data["description"], data["visited"], last_visit_date))
    conn.commit()
    conn.close()
    return f"Бар '{data['name']}' успешно добавлен в базу данных!"

def get_last_visit(bar_name):
    """Получает дату последнего визита в бар по названию"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT last_visit_date FROM bars WHERE name = ?", (bar_name,))
    row = cursor.fetchone()
    conn.close()

    if row is None:
        return None  # Бар не найден
    return row[0] or ""  # Вернёт дату или пустую строку, если даты нет


def get_random_bar_by_category(category):
    """Получает случайный бар по категории"""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    if category == "not_visited":
        # Выбираем бары, которые не посещали (visited = 0)
        cursor.execute("SELECT name, description FROM bars WHERE visited = 0")
    elif category == "visited":
        # Выбираем бары, которые посещали (visited = 1)
        cursor.execute("SELECT name, description FROM bars WHERE visited = 1")
    elif category == "all":
        # Выбираем все бары
        cursor.execute("SELECT name, description FROM bars")

    rows = cursor.fetchall()
    conn.close()

    if rows:
        return random.choice(rows)  # Возвращаем случайный бар
    return None  # Если баров нет, возвращаем None

def get_bar_by_name(bar_name):
    """Ищет бар по названию."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bars WHERE name = ?", (bar_name,))
    row = cursor.fetchone()
    conn.close()
    return row  # Вернёт данные о баре или None, если бара нет

def update_bar_visit(bar_name, visit_date):
    """Обновляет дату посещения бара."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    UPDATE bars
    SET last_visit_date = ?, visited = 1
    WHERE name = ?
    """, (visit_date, bar_name))
    conn.commit()
    conn.close()
