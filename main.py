import os
import telebot
from telebot import types
from apscheduler.schedulers.background import BackgroundScheduler
import mysql.connector
from database_config import get_db_cursor, API_TOKEN
from datetime import datetime, timedelta

bot = telebot.TeleBot(API_TOKEN)
scheduler = BackgroundScheduler()
scheduler.start()

WEBINAR_TIME = datetime(2025, 4, 12, 18, 0)  # Киев 18:00

@bot.message_handler(commands=['start'])
def send_welcome(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    btn = types.KeyboardButton("Зарегистрироваться")
    markup.add(btn)

    welcome_text = (
        "Привет! 👋\n"
        "На вебинаре «Автоматизируй рутину с ИИ» я покажу, как использовать искусственный интеллект для автоматизации процессов и личных задач.\n\n"
        "Вебинар пройдёт сегодня:\n"
        "12.04.2025 в 17:00 Варшава | 18:00 Киев.\n\n"
        "Никакой лишней теории — только практические инструменты, которые уже сегодня помогут сэкономить время и ресурсы. Вы узнаете:\n\n"
        "✅ Как автоматизировать рутинные задачи без программирования\n"
        "✅ Какие ИИ-инструменты помогут в работе и жизни\n"
        "✅ Реальные кейсы, которые я ежедневно использую в своих компаниях\n\n"
        "Нажмите «Зарегистрироваться» и получите подарок 🎁 — 30-минутный бесплатный урок:\n"
        "«Как автоматизировать работу юриста и обработку документов с помощью ИИ»"
    )
    bot.send_message(message.chat.id, welcome_text, reply_markup=markup)

@bot.message_handler(func=lambda message: message.text == "Зарегистрироваться")
def register(message):
    conn, cursor = get_db_cursor()
    cursor.execute("INSERT IGNORE INTO users (user_id) VALUES (%s)", (message.chat.id,))
    conn.commit()
    cursor.close()
    conn.close()

    bot.send_message(message.chat.id, "✅ Вы зарегистрированы на вебинар! Напомним за 15 минут до начала.")

def notify_users():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT user_id FROM users")
    users = cursor.fetchall()
    cursor.close()
    conn.close()

    for user in users:
        bot.send_message(user[0], "⏰ Напоминание: Вебинар начнется через 15 минут!")

# Расписание задачи
reminder_time = WEBINAR_TIME - timedelta(minutes=15)
scheduler.add_job(notify_users, trigger='date', run_date=reminder_time)

def main():
    print("Бот запущен...")
    bot.infinity_polling()

if __name__ == '__main__':
    main()
