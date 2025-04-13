import os
from requests import get
import logging
import time
import telebot
from telebot import types
import mysql.connector
import matplotlib.pyplot as plt
import re
from database_config import get_db_cursor, api_token

API_TOKEN = api_token

categories = {
    "Birthday": 1,
    "Anniversary": 2,
    "Meeting": 3,
    "Task": 4,
    "Other": 5
}

categoryId = 0
date = ''
time_string = ''
reminder_text = ''
user_id = 0

bot = telebot.TeleBot(API_TOKEN)

@bot.message_handler(commands=['start'])
def Send_Welcome(message):
    global user_id
    user_id = message.chat.id
    conn, cursor = get_db_cursor()

    username = message.chat.username or ""

    query = """
        INSERT INTO users (user_id, username)
        VALUES (%s, %s)
        ON DUPLICATE KEY UPDATE username=%s
    """
    val = (user_id, username, username)
    cursor.execute(query, val)
    conn.commit()

    bot.send_message(user_id, "✅ You have been registered for the webinar!")

    cursor.close()
    conn.close()

def main():
    print("Bot is polling...")
    bot.polling(none_stop=True)

if __name__ == "__main__":
    main()
