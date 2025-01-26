from telebot import TeleBot
from database.db_helper import get_last_visit

# Словарь для отслеживания пользователей, ожидающих ответ
user_states = {}


def register_last_visit(bot: TeleBot):
    @bot.message_handler(commands=['last_visit'])
    def start_last_visit(message):
        user_id = message.from_user.id
        user_states[user_id] = "awaiting_bar_name"  # Сохраняем состояние пользователя
        bot.reply_to(message, "Я могу подсказать дату последнего визита в конкретный бар. Какой бар проверить?")

    @bot.message_handler(func=lambda msg: user_states.get(msg.from_user.id) == "awaiting_bar_name")
    def process_bar_name(message):
        user_id = message.from_user.id
        bar_name = message.text.strip()

        # Ищем дату последнего визита
        result = get_last_visit(bar_name)

        if result is None:
            bot.reply_to(message,
                         "Бар не найден в базе. Возможно вы ошиблись в названии сейчас или при добавлении бара.")
        elif result == "":
            bot.reply_to(message, "Дата посещения этого бара не записана в базе. Не забывайте обновлять информацию.")
        else:
            bot.reply_to(message, f"Последний визит в бар '{bar_name}' был: {result}.")

        # Удаляем пользователя из словаря состояний
        user_states.pop(user_id, None)
