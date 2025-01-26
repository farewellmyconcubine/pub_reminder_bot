import sqlite3

DB_NAME = "bars.db"

def view_bars():
    """Выводит все записи из таблицы bars"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM bars")
    rows = cursor.fetchall()
    conn.close()

    if rows:
        print("Список баров:")
        for row in rows:
            print(f"ID: {row[0]}, Name: {row[1]}, Description: {row[2]}, Visited: {row[3]}, Last Visit: {row[4]}")
    else:
        print("База данных пуста.")

def delete_bar(bar_id):
    """Удаляет запись из таблицы bars по ID"""
    conn = sqlite3.connect(DB_NAME)
    cursor = conn.cursor()
    cursor.execute("DELETE FROM bars WHERE id = ?", (bar_id,))
    conn.commit()
    conn.close()

    if cursor.rowcount > 0:
        print(f"Запись с ID {bar_id} успешно удалена.")
    else:
        print(f"Запись с ID {bar_id} не найдена.")

if __name__ == "__main__":
    print("Управление базой данных")
    print("1. Просмотреть записи")
    print("2. Удалить запись по ID")
    choice = input("Выберите действие (1 или 2): ")

    if choice == "1":
        view_bars()
    elif choice == "2":
        bar_id = input("Введите ID бара для удаления: ")
        if bar_id.isdigit():
            delete_bar(int(bar_id))
        else:
            print("Некорректный ID. Попробуйте снова.")
    else:
        print("Неверный выбор.")
