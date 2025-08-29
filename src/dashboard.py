"""
dashboard.py
Streamlit dashboard that shows logs, alerts, and simple analytics.

Run:
    streamlit run dashboard.py
"""
import sqlite3
import pandas as pd
import streamlit as st
import plotly.express as px

DB_PATH = "logs.db"

st.set_page_config(page_title="Mini SIEM + UEBA", layout="wide")
st.title("🛡️ AI-Powered Mini SIEM with UEBA")

# --- Ensure alerts table exists ---
def ensure_alerts_table():
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    cursor.execute("""
    CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        timestamp TEXT,
        severity TEXT,
        message TEXT,
        is_anomaly INTEGER DEFAULT 0
    );
    """)
    conn.commit()
    conn.close()

ensure_alerts_table()

# --- Data Loaders ---
@st.cache_data(ttl=3)
def load_logs(limit=500):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM logs ORDER BY id DESC LIMIT {limit}", conn)
    conn.close()
    return df

@st.cache_data(ttl=3)
def load_alerts(limit=200):
    conn = sqlite3.connect(DB_PATH)
    df = pd.read_sql_query(f"SELECT * FROM alerts ORDER BY id DESC LIMIT {limit}", conn)
    conn.close()
    return df

# --- Tabs ---
tab1, tab2, tab3 = st.tabs(["📜 Logs", "🚨 Alerts", "📊 Analytics"])

# Logs tab
with tab1:
    st.subheader("Recent Logs")
    logs = load_logs(500)
    if logs.empty:
        st.info("No logs found. Generate logs with `log_generator.py` and run `log_parser.py`.")
    else:
        st.dataframe(logs, use_container_width=True, height=350)

# Alerts tab
with tab2:
    st.subheader("Active Alerts")
    alerts = load_alerts(200)
    if alerts.empty:
        st.info("No alerts. Run `siem_rules.py` and `ueba_model.py` to generate alerts.")
    else:
        st.dataframe(alerts, use_container_width=True, height=350)
        if "is_anomaly" in alerts.columns:
            anoms = alerts[alerts["is_anomaly"] == 1]
            if not anoms.empty:
                st.warning(f"⚠️ {len(anoms)} anomalies detected (latest {min(20, len(anoms))} shown).")

# Analytics tab
with tab3:
    st.subheader("Analytics & Visualizations")
    logs = load_logs(1000)
    if logs.empty:
        st.info("No logs to visualize.")
    else:
        # Events per user (top 10)
        if "user" in logs.columns:
            user_counts = logs["user"].value_counts().reset_index().head(10)
            user_counts.columns = ["user", "event_count"]
            fig1 = px.bar(user_counts, x="user", y="event_count", title="Top Users by Event Count")
            st.plotly_chart(fig1, use_container_width=True)

        # Event distribution
        if "event" in logs.columns:
            event_counts = logs["event"].value_counts().reset_index()
            event_counts.columns = ["event", "count"]
            fig2 = px.pie(event_counts, names="event", values="count", title="Event Distribution")
            st.plotly_chart(fig2, use_container_width=True)

        # Event rate over time
        if "timestamp" in logs.columns:
            logs["timestamp"] = pd.to_datetime(logs["timestamp"], errors="coerce")
            time_counts = logs.groupby(pd.Grouper(key="timestamp", freq="1min")).size().reset_index(name="count")
            fig3 = px.line(time_counts, x="timestamp", y="count", title="Events Over Time")
            st.plotly_chart(fig3, use_container_width=True)
