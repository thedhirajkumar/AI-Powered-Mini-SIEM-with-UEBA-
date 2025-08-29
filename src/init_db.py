import sqlite3

# Connect to SQLite (creates logs.db if it doesn't exist)
conn = sqlite3.connect("logs.db")
cursor = conn.cursor()

# Create logs table
cursor.execute("""
CREATE TABLE IF NOT EXISTS logs (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    timestamp TEXT,
    user TEXT,
    action TEXT,
    status TEXT,
    source_ip TEXT
)
""")

# Insert some sample logs
sample_logs = [
    ("2025-08-29 10:00:00", "alice", "login", "failed", "192.168.1.10"),
    ("2025-08-29 10:02:00", "bob", "login", "success", "192.168.1.11"),
    ("2025-08-29 10:05:00", "alice", "login", "failed", "192.168.1.10"),
    ("2025-08-29 10:07:00", "alice", "login", "failed", "192.168.1.10"),
    ("2025-08-29 10:08:00", "eve", "file_access", "success", "192.168.1.12"),
]

cursor.executemany(
    "INSERT INTO logs (timestamp, user, action, status, source_ip) VALUES (?, ?, ?, ?, ?)",
    sample_logs
)

conn.commit()
conn.close()

print("✅ Database initialized with sample logs.")
