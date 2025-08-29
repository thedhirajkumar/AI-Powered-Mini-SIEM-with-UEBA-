import sqlite3
from datetime import datetime

DB_PATH = "logs.db"

def insert_dummy_alerts():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    dummy_alerts = [
        (datetime.now().isoformat(), "HIGH", "Suspicious login attempt detected", 1),
        (datetime.now().isoformat(), "MEDIUM", "Multiple failed logins from same IP", 0),
        (datetime.now().isoformat(), "LOW", "Unusual file access pattern", 1),
    ]

    cursor.executemany(
        "INSERT INTO alerts (timestamp, severity, message, is_anomaly) VALUES (?, ?, ?, ?)",
        dummy_alerts
    )
    conn.commit()
    conn.close()
    print("✅ Inserted dummy alerts into alerts table.")

if __name__ == "__main__":
    insert_dummy_alerts()
