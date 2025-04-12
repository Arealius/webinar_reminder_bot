import os
import re
import time
import logging
from telebot import TeleBot, types
from apscheduler.schedulers.background import BackgroundScheduler
from database_config import mydb, api_token

bot = TeleBot(api_token)

def get_db_cursor():
    connection = mydb
    return connection, connection.cursor(buffered=True)

@bot.message_handler(commands=['start'])
def send_welcome(message):
    conn, cursor = get_db_cursor()
    user_id = message.from_user.id
    username = message.from_user.username or ""
    
    cursor.execute("INSERT INTO users (user_id, username) VALUES (%s, %s) ON DUPLICATE KEY UPDATE username=%s", (user_id, username, username))
    conn.commit()
    bot.reply_to(message, "✅ You are registered for the webinar!")

# Пример уведомления (можно адаптировать под время вебинара)
def send_reminders():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT user_id FROM users")
    for (user_id,) in cursor.fetchall():
        bot.send_message(user_id, "⏰ Reminder: The webinar starts in 30 minutes!")
    conn.close()

# Планировщик уведомлений (можно настроить на нужное время)
scheduler = BackgroundScheduler()
# scheduler.add_job(send_reminders, 'date', run_date='2025-04-13 18:00:00')  # Пример
scheduler.start()

# ВАЖНО: запуск бота
bot.infinity_polling()
