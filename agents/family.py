import sqlite3
from datetime import datetime

class FamilyAgent:
    def __init__(self, db_path="db/memory.sqlite"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS alerts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                message TEXT
            )
        """)
        self.conn.commit()

    def send_alert(self, message):
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        print(f" Family Alert: {message}")
        self.cursor.execute("INSERT INTO alerts (timestamp, message) VALUES (?, ?)", (now, message))
        self.conn.commit()