"""
siem_rules.py
Simple rule-based correlation to produce alerts and write them to alerts table.

Usage:
    python siem_rules.py
"""
import sqlite3
from datetime import datetime

DB_PATH = "db.sqlite"

def ensure_alerts_table(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,        -- 'rule' or 'ueba'
        user TEXT,
        ip TEXT,
        score REAL,
        is_anomaly INTEGER,
        created_at TEXT,
        note TEXT
    )
    """)
    conn.commit()

def run_rules(conn):
    cur = conn.cursor()
    # 1) Brute-force detection: >=5 failed logins for same user
    cur.execute("""
    SELECT user, COUNT(*) as fail_count
    FROM logs
    WHERE event='login_failed'
    GROUP BY user
    HAVING fail_count >= 5
    """)
    for user, fail_count in cur.fetchall():
        note = f"Brute-force: {fail_count} failed logins"
        cur.execute("INSERT INTO alerts (source,user,ip,score,is_anomaly,created_at,note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("rule", user, None, None, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), note))

    # 2) Suspicious IP: >= 20 events from same IP
    cur.execute("""
    SELECT ip, COUNT(*) as ev_count
    FROM logs
    GROUP BY ip
    HAVING ev_count >= 20
    """)
    for ip, ev_count in cur.fetchall():
        note = f"Suspicious IP activity: {ev_count} events"
        cur.execute("INSERT INTO alerts (source,user,ip,score,is_anomaly,created_at,note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("rule", None, ip, None, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), note))

    # 3) Multiple config changes by same user (>=3)
    cur.execute("""
    SELECT user, COUNT(*) as change_count
    FROM logs
    WHERE event='config_change'
    GROUP BY user
    HAVING change_count >= 3
    """)
    for user, change_count in cur.fetchall():
        note = f"Multiple config changes: {change_count}"
        cur.execute("INSERT INTO alerts (source,user,ip,score,is_anomaly,created_at,note) VALUES (?, ?, ?, ?, ?, ?, ?)",
                    ("rule", user, None, None, 1, datetime.now().strftime("%Y-%m-%d %H:%M:%S"), note))

    conn.commit()

def main():
    conn = sqlite3.connect(DB_PATH)
    ensure_alerts_table(conn)
    run_rules(conn)
    conn.close()
    print("SIEM rules executed and alerts inserted (if any).")

if __name__ == "__main__":
    main()
