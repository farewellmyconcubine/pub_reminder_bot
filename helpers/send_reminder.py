import telebot
import os

# Получение токена и ID чата из переменных окружения
BOT_TOKEN = os.getenv("BOT_TOKEN")
CHAT_ID = os.getenv("CHAT_ID")

bot = telebot.TeleBot(BOT_TOKEN)

def send_reminder():
    bot.send_message(CHAT_ID, "Wake up! It's the first of the month! 🐄🐄🐄/nВыйдите на улицу потрогайте траву, в бар сходите что-ли.")

if __name__ == "__main__":
    send_reminder()
