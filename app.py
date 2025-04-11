from agents.reminder import ReminderAgent
from agents.safety import SafetyAgent
from agents.health import HealthAgent
from agents.social import SocialAgent
from agents.family import FamilyAgent
from agents.doctor import DoctorAgent
import sqlite3
import time
import random

#  Function to set up SQLite database and reminders table
def setup_db():
    conn = sqlite3.connect("db/memory.sqlite")
    cursor = conn.cursor()

    # Create the reminders table if it doesn't exist
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS reminders (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            time TEXT NOT NULL,
            message TEXT NOT NULL,
            language TEXT NOT NULL
        )
    ''')

    # Insert sample reminder data (with unique time & message combos)
    cursor.execute("INSERT OR IGNORE INTO reminders (time, message, language) VALUES (?, ?, ?)",
                   ("14:30", "மருந்து எடுத்துக்கொள்ளுங்கள்", "ta"))
    cursor.execute("INSERT OR IGNORE INTO reminders (time, message, language) VALUES (?, ?, ?)",
                   ("14:30", "अपनी दवाई लीजिए", "hi"))
    cursor.execute("INSERT OR IGNORE INTO reminders (time, message, language) VALUES (?, ?, ?)",
                   ("14:30", "మీ మందును తీసుకోండి", "te"))

    conn.commit()
    conn.close()

# ✅ Initialize database
setup_db()

# ✅ Initialize all agent modules
reminder = ReminderAgent()
safety = SafetyAgent()
health = HealthAgent()
social = SocialAgent()
family = FamilyAgent()
doctor = DoctorAgent()

# ✅ Main loop to simulate behavior
print(" Starting Elderly Care AI...")
while True:
    reminder.check_and_remind()
    
    if safety.check_inactivity():
        family.send_alert("Inactivity detected for 5 minutes!")
        doctor.consult("Patient inactive for 5 minutes. Advice?")
    
    health_pred = health.monitor_health()
    if health_pred:
        family.send_alert("Critical health condition detected!")
        doctor.consult("Critical vitals detected. What to do?")
    
    social.cheer_up(random.choice(["ta", "hi", "te"]))

    time.sleep(60)  # Wait for 60 seconds before repeating


