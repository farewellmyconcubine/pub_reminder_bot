from telebot import TeleBot
from database.db_helper import save_bar  # Импортируем save_bar

user_data = {}


def register_add_bar(bot: TeleBot):
    @bot.message_handler(commands=['add_bar'])
    def start_add_bar(message):
        user_id = message.from_user.id
        user_data[user_id] = {"step": 1}
        bot.reply_to(message, "Как называется бар?")

    @bot.message_handler(func=lambda msg: msg.from_user.id in user_data and user_data[msg.from_user.id]["step"] == 1)
    def get_bar_name(message):
        user_id = message.from_user.id
        user_data[user_id]["name"] = message.text
        user_data[user_id]["step"] = 2
        bot.reply_to(message, "Напишите описание бара (или оставьте пустым, отправив '-')")

    @bot.message_handler(func=lambda msg: msg.from_user.id in user_data and user_data[msg.from_user.id]["step"] == 2)
    def get_bar_description(message):
        user_id = message.from_user.id
        description = message.text if message.text != "-" else "Описание отсутствует"
        user_data[user_id]["description"] = description
        user_data[user_id]["step"] = 3
        bot.reply_to(message, "Вы уже были в этом баре? (Ответьте 'Да' или 'Нет')")

    @bot.message_handler(func=lambda msg: msg.from_user.id in user_data and user_data[msg.from_user.id]["step"] == 3)
    def get_bar_visited(message):
        user_id = message.from_user.id
        answer = message.text.lower()
        if answer in ["да", "нет"]:
            user_data[user_id]["visited"] = 1 if answer == "да" else 0
            if answer == "да":
                user_data[user_id]["step"] = 4
                bot.reply_to(message,
                             "Введите дату последнего визита или '-' если хотите пропустить")
            else:
                confirmation_message = save_bar(user_data[user_id], None)  # Исправленный вызов
                bot.reply_to(message, confirmation_message)
                user_data.pop(user_id)
        else:
            bot.reply_to(message, "Пожалуйста, ответьте 'Да' или 'Нет'.")

    @bot.message_handler(func=lambda msg: msg.from_user.id in user_data and user_data[msg.from_user.id]["step"] == 4)
    def get_last_visit_date(message):
        user_id = message.from_user.id
        date = message.text if message.text != "-" else None
        confirmation_message = save_bar(user_data[user_id], date)  # Исправленный вызов
        bot.reply_to(message, confirmation_message)
        user_data.pop(user_id)
