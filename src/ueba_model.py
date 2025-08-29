"""
ueba_model.py
UEBA using IsolationForest. Reads logs table, computes per-user features, runs IsolationForest,
and inserts detection results into alerts table with source='ueba'.

Usage:
    python ueba_model.py
"""
import sqlite3
from datetime import datetime
import pandas as pd
import numpy as np
from sklearn.ensemble import IsolationForest

DB_PATH = "db.sqlite"

def ensure_alerts_table(conn):
    cur = conn.cursor()
    cur.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        source TEXT,
        user TEXT,
        ip TEXT,
        score REAL,
        is_anomaly INTEGER,
        created_at TEXT,
        note TEXT
    )
    """)
    conn.commit()

def load_logs(conn):
    return pd.read_sql_query("SELECT * FROM logs", conn, parse_dates=["timestamp"])

def build_features(df):
    # per-user features
    df['timestamp'] = pd.to_datetime(df['timestamp'], errors='coerce')
    df = df.dropna(subset=['timestamp'])
    group = df.groupby('user')
    rows = []
    for user, g in group:
        total_events = len(g)
        failed_logins = (g['event'] == 'login_failed').sum()
        success_logins = (g['event'] == 'login_success').sum()
        unique_ips = g['ip'].nunique()
        tmin = g['timestamp'].min()
        tmax = g['timestamp'].max()
        duration_minutes = max((tmax - tmin).total_seconds() / 60.0, 1.0)
        events_per_minute = total_events / duration_minutes
        rows.append({
            'user': user,
            'total_events': total_events,
            'failed_logins': failed_logins,
            'success_logins': success_logins,
            'unique_ips': unique_ips,
            'events_per_minute': events_per_minute
        })
    feat_df = pd.DataFrame(rows).set_index('user')
    if feat_df.empty:
        return feat_df
    feat_df = feat_df.fillna(0)
    return feat_df

def run_ueba(conn, contamination=0.1):
    df = load_logs(conn)
    feat_df = build_features(df)
    if feat_df.empty:
        print("No users/logs to analyze.")
        return

    X = feat_df.values
    iso = IsolationForest(random_state=42, n_estimators=100, contamination=contamination)
    iso.fit(X)
    scores = iso.decision_function(X)
    preds = iso.predict(X)  # -1 anomaly, 1 normal

    cur = conn.cursor()
    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    for i, user in enumerate(feat_df.index):
        score = float(scores[i])
        is_anom = int(preds[i] == -1)
        row = feat_df.loc[user]
        note = None
        if is_anom:
            note = f"UEBA anomaly: failed_logins={int(row['failed_logins'])}, unique_ips={int(row['unique_ips'])}, events_per_minute={row['events_per_minute']:.2f}"
        cur.execute("""
            INSERT INTO alerts (source,user,ip,score,is_anomaly,created_at,note)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        """, ("ueba", user, None, score, is_anom, now, note))
    conn.commit()
    print(f"UEBA executed: inserted {len(feat_df)} UEBA results into alerts table.")

def main():
    conn = sqlite3.connect(DB_PATH)
    ensure_alerts_table(conn)
    run_ueba(conn, contamination=0.1)
    conn.close()

if __name__ == "__main__":
    main()
