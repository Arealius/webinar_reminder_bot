import os
from requests import get
import logging
import telebot
import matplotlib.pyplot as plt
from telebot import types
import mysql.connector
from apscheduler.schedulers.background import BackgroundScheduler
import re
from database_config import get_db_cursor, API_TOKEN

bot = telebot.TeleBot(API_TOKEN)

# ✅ Добавляем обработчик /start
@bot.message_handler(commands=['start'])
def handle_start(message):
    bot.send_message(message.chat.id, "Привет! Ты успешно запустил бота. 🔔 Зарегистрируйся на вебинар!")

categories = {
    "Birthday": 1,
    "Anniversary": 2,
    "Meeting": 3,
    "Task": 4,
    "Other": 5
}

def reminder_text(event_name, event_time):
    return f"🔔 Напоминание: {event_name} запланировано на {event_time}"

def send_reminders():
    conn, cursor = get_db_cursor()
    cursor.execute("SELECT user_id, event_name, event_time FROM reminders WHERE notified = 0")
    reminders = cursor.fetchall()
    for user_id, event_name, event_time in reminders:
        text = reminder_text(event_name, event_time)
        bot.send_message(user_id, text)
        cursor.execute("UPDATE reminders SET notified = 1 WHERE user_id = %s AND event_name = %s", (user_id, event_name))
    conn.commit()
    cursor.close()
    conn.close()

scheduler = BackgroundScheduler()
scheduler.add_job(send_reminders, 'interval', minutes=1)
scheduler.start()

bot.polling(none_stop=True)
