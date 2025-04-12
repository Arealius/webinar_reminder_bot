import telebot
from telebot import types
import time
from datetime import datetime, timedelta
from apscheduler.schedulers.background import BackgroundScheduler
from database_config import get_db_cursor, API_TOKEN

bot = telebot.TeleBot(API_TOKEN)
scheduler = BackgroundScheduler()
scheduler.start()

WEBINAR_TIME = datetime(2025, 4, 13, 20, 0)  # Установи своё время

@bot.message_handler(commands=['start'])
def start(message):
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT * FROM users WHERE chat_id = %s", (message.chat.id,))
    if not cursor.fetchone():
        cursor.execute("INSERT INTO users (chat_id) VALUES (%s)", (message.chat.id,))
        conn.commit()
        bot.send_message(message.chat.id, "Вы зарегистрированы на вебинар!")
        schedule_reminder(message.chat.id)
    else:
        bot.send_message(message.chat.id, "Вы уже зарегистрированы.")
    cursor.close()
    conn.close()

def schedule_reminder(chat_id):
    reminder_time = WEBINAR_TIME - timedelta(minutes=30)
    scheduler.add_job(lambda: bot.send_message(chat_id, "⏰ Напоминание: вебинар начнётся через 30 минут!"),
                      trigger='date', run_date=reminder_time)

bot.polling()
