import sqlite3
from datetime import datetime
from utils.tts import speak

class ReminderAgent:
    def __init__(self, db_path="db/memory.sqlite"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS reminders (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                time TEXT,
                message TEXT,
                language TEXT
            )
        """)
        self.conn.commit()

    def check_and_remind(self):
        now = datetime.now().strftime("%H:%M")
        self.cursor.execute("SELECT message, language FROM reminders WHERE time = ?", (now,))
        reminders = self.cursor.fetchall()
        for message, lang in reminders:
            print(f" Reminder: {message}")
            speak(message, lang)