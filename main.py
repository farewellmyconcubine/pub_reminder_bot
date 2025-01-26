from telebot import TeleBot
from commands.add_bar import register_add_bar
from commands.last_visit import register_last_visit
from commands.random_bar import register_random_bar
from commands.reg_visit import register_reg_visit
from database.db_helper import init_db
from dotenv import load_dotenv
import os

# Загрузка переменных из .env
load_dotenv()
API_TOKEN = os.getenv("BOT_TOKEN")

if not API_TOKEN:
    raise ValueError("Не найден API токен бота. Убедитесь, что он указан в файле .env")

# Инициализация бота
bot = TeleBot(API_TOKEN)

# Инициализация базы данных
init_db()

# Регистрация команд
register_add_bar(bot)
register_last_visit(bot)
register_random_bar(bot)
register_reg_visit(bot)

# Запуск бота
if __name__ == "__main__":
    print("Бот запущен...")
    bot.polling(non_stop=True, timeout=100)
