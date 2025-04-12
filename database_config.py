import os
import mysql.connector

def get_db_cursor():
    conn = mysql.connector.connect(
        host=os.environ.get("DB_HOST"),
        user=os.environ.get("DB_USER"),
        password=os.environ.get("DB_PASSWORD"),
        database=os.environ.get("DB_NAME")
    )
    return conn, conn.cursor(buffered=True)

API_TOKEN = os.environ.get("BOT_TOKEN")
