import sqlite3
from datetime import datetime, timedelta

class SafetyAgent:
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
        self.last_movement = datetime.now()

    def simulate_motion(self):
        self.last_movement = datetime.now()

    def check_inactivity(self):
        now = datetime.now()
        delta = now - self.last_movement
        if delta > timedelta(minutes=5):
            message = "Inactivity detected for 5 minutes!"
            print(f"⚠️ {message}")
            self.cursor.execute("INSERT INTO alerts (timestamp, message) VALUES (?, ?)",
                               (now.strftime("%Y-%m-%d %H:%M:%S"), message))
            self.conn.commit()
            return True
        return False