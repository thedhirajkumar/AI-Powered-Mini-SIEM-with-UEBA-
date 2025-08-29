# 🛡️ AI-Powered Mini SIEM with UEBA

A lightweight **Security Information and Event Management (SIEM)** system with **User & Entity Behavior Analytics (UEBA)**.  
It collects logs, applies both **rule-based detection** and **ML-driven anomaly detection**, and displays results in a real-time **Streamlit + Plotly dashboard**.

---

## 🚀 Features
- 📜 **Log Management** – Collects and stores logs in SQLite  
- 🚨 **Alerts Engine** – Rule-based detection (e.g., brute-force login attempts)  
- 🤖 **UEBA (ML Model)** – Detects anomalies using Isolation Forest  
- 📊 **Real-Time Dashboard** – Built with Streamlit + Plotly  
- 🗄️ **SQLite Backend** – Lightweight, portable storage for logs and alerts  

---

## 🏗️ Architecture
1. **Logs** → Stored in `logs` table  
2. **Detection** →  
   - Rule-based detection via `siem_rules.py`  
   - ML-based anomaly detection via `ueba_model.py`  
   - Alerts stored in `alerts` table  
3. **Dashboard** → `src/dashboard.py` shows:
   - Logs tab → Raw logs  
   - Alerts tab → Alerts & anomalies  
   - Analytics tab → User activity, event distribution, time trends  

---

## ⚙️ Tech Stack
- **Python** (Streamlit, Pandas, Numpy, Scikit-learn, Plotly)  
- **SQLite** (lightweight database for logs & alerts)  
- **Streamlit** (real-time dashboard)  

---

## Future Improvements

Replace SQLite with PostgreSQL / Elasticsearch

Use Kafka for real-time log ingestion

Deploy ML model as a microservice

Add role-based access control for SOC analysts

## Author

👨‍💻 Developed by Dhiraj kumar

🎯 Built for learning SIEM concepts, anomaly detection, and full-stack security analytics.
