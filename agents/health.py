import joblib
import sqlite3
from datetime import datetime
import random

class HealthAgent:
    def __init__(self, db_path="db/memory.sqlite"):
        self.conn = sqlite3.connect(db_path)
        self.cursor = self.conn.cursor()
        self.cursor.execute("""
            CREATE TABLE IF NOT EXISTS health_logs (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                timestamp TEXT,
                heart_rate INTEGER,
                bp_systolic INTEGER,
                bp_diastolic INTEGER,
                is_critical INTEGER
            )
        """)
        self.conn.commit()
        try:
            self.model = joblib.load("./health_model.pkl")
        except FileNotFoundError:
            print("❌ Run 'train_health_model.py' first to generate health_model.pkl")
            exit(1)

    def monitor_health(self):
        # Simulated input (replace with IoT later)
        hr = random.randint(65, 110)
        sys = random.randint(110, 160)
        dia = random.randint(70, 100)
        spo2 = random.randint(90, 100)

        prediction = self.model.predict([[hr, sys, dia, spo2]])[0]
        now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.cursor.execute("""
            INSERT INTO health_logs (timestamp, heart_rate, bp_systolic, bp_diastolic, is_critical)
            VALUES (?, ?, ?, ?, ?)
        """, (now, hr, sys, dia, int(prediction)))
        self.conn.commit()
        print(f" Health: HR={hr}, BP={sys}/{dia}, Critical={bool(prediction)}")
        return prediction