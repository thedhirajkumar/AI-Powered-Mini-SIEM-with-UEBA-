"""
log_parser.py
Parse JSON lines from logs.json (or STDIN) and insert into SQLite logs table.

Usage:
    python log_generator.py > logs.json
    python log_parser.py logs.json
Or:
    python log_generator.py | python log_parser.py
"""
import sqlite3
import json
import sys
import os

DB_PATH = "db.sqlite"
LOG_SOURCE = sys.argv[1] if len(sys.argv) > 1 else None

def ensure_db(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS logs (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        user TEXT,
        ip TEXT,
        event TEXT
    )
    """)
    conn.commit()

def insert_log(conn, log):
    cur = conn.cursor()
    cur.execute(
        "INSERT INTO logs (timestamp, user, ip, event) VALUES (?, ?, ?, ?)",
        (log.get("timestamp"), log.get("user"), log.get("ip"), log.get("event"))
    )

def main():
    conn = sqlite3.connect(DB_PATH)
    ensure_db(conn)
    # Read from file if provided, else from stdin
    if LOG_SOURCE and os.path.exists(LOG_SOURCE):
        source = open(LOG_SOURCE, "r")
    else:
        source = sys.stdin

    count = 0
    for line in source:
        line = line.strip()
        if not line:
            continue
        try:
            log = json.loads(line)
            insert_log(conn, log)
            count += 1
        except json.JSONDecodeError:
            continue
    conn.commit()
    if LOG_SOURCE and os.path.exists(LOG_SOURCE):
        source.close()
    conn.close()
    print(f"Inserted {count} logs into {DB_PATH}")

if __name__ == "__main__":
    main()
