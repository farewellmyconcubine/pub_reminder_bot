from telebot import TeleBot
from database.db_helper import get_bar_by_name, update_bar_visit

# Словарь для хранения состояния пользователей
user_states = {}

def register_reg_visit(bot: TeleBot):
    @bot.message_handler(commands=['reg_visit'])
    def ask_bar_name(message):
        user_id = message.from_user.id
        user_states[user_id] = {"step": "awaiting_bar_name"}
        bot.reply_to(message, "Введите название бара, чтобы добавить дату посещения:")

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id, {}).get("step") == "awaiting_bar_name")
    def process_bar_name(message):
        user_id = message.from_user.id
        bar_name = message.text.strip()
        bar = get_bar_by_name(bar_name)

        if bar:
            user_states[user_id] = {"step": "awaiting_visit_date", "bar_name": bar_name}
            bot.reply_to(message, f"Бар '{bar_name}' найден в базе. Введите дату посещения (например, 25-01-2025):")
        else:
            user_states.pop(user_id, None)  # Сбрасываем состояние
            bot.reply_to(message, f"Бар '{bar_name}' не найден в базе. Вы можете добавить его с помощью команды /add_bar.")

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id, {}).get("step") == "awaiting_visit_date")
    def process_visit_date(message):
        user_id = message.from_user.id
        visit_date = message.text.strip()
        bar_name = user_states[user_id]["bar_name"]

        valid_date = validate_date(visit_date)
        if valid_date:
            update_bar_visit(bar_name, valid_date)
            bot.reply_to(message, f"Дата посещения для бара '{bar_name}' успешно обновлена в базе на {visit_date}.")
            user_states.pop(user_id, None)  # Сбрасываем состояние
        else:
            bot.reply_to(message, "Неверный формат даты. Убедитесь, что дата введена в формате ДД-ММ-ГГГГ.")

def validate_date(date_text):
    """
    Проверяет, является ли строка корректной датой в формате ДД-ММ-ГГГГ.
    Возвращает дату в формате ГГГГ-ММ-ДД для записи в базу.
    """
    from datetime import datetime
    try:
        # Преобразуем из ДД-ММ-ГГГГ в объект даты
        date_obj = datetime.strptime(date_text, "%d-%m-%Y")
        # Возвращаем строку в формате ГГГГ-ММ-ДД для базы данных
        return date_obj.strftime("%Y-%m-%d")
    except ValueError:
        return None
