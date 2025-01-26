from telebot import TeleBot, types
from database.db_helper import get_random_bar_by_category

def register_random_bar(bot: TeleBot):
    @bot.message_handler(commands=['random_bar'])
    def ask_category(message):
        # Создаём инлайн-кнопки
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(
            types.InlineKeyboardButton("Не посещали", callback_data=f"not_visited:{message.chat.id}"),
            types.InlineKeyboardButton("Посещённые", callback_data=f"visited:{message.chat.id}"),
            types.InlineKeyboardButton("Все вместе", callback_data=f"all:{message.chat.id}")
        )
        bot.reply_to(message, "Из каких баров выбирать?", reply_markup=keyboard)

    @bot.callback_query_handler(func=lambda call: call.data.split(":")[0] in ["not_visited", "visited", "all"])
    def handle_category(call):
        data = call.data.split(":")
        category = data[0]
        chat_id = int(data[1])  # Получаем ID чата из callback_data
        user_name = call.from_user.first_name or call.from_user.username or "Кто-то"  # Имя пользователя

        # Получаем случайный бар по категории
        random_bar = get_random_bar_by_category(category)

        if random_bar:
            name, description = random_bar
            bot.send_message(
                chat_id,
                f"{user_name} запросил случайный бар\n"
                f"Рекомендуем посетить бар: {name}\nОписание: {description}"
            )
        else:
            bot.send_message(chat_id, f"{user_name}, в выбранной категории нет баров. Попробуйте другую категорию.")

        # Уведомляем Telegram, что запрос обработан
        bot.answer_callback_query(call.id)
