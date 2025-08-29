"""
log_generator.py
Generate synthetic security logs and print JSON lines to stdout (or file redirect).
Usage:
    python log_generator.py > logs.json
"""
import random
import time
import json
from datetime import datetime, timedelta

USERS = ["alice", "bob", "charlie", "david", "eve", "mallory"]
IPS = ["192.168.1.10", "192.168.1.20", "10.0.0.5", "172.16.0.3", "203.0.113.5"]
EVENTS = ["login_success", "login_failed", "file_access", "config_change"]

def generate_log():
    # Slightly biased distribution so we sometimes get many failed logins for 'mallory'
    user = random.choices(USERS, weights=[15,15,15,15,15,5])[0]
    if user == "mallory" and random.random() < 0.8:
        event = "login_failed"
        ip = "198.51.100.7"  # attacker IP
    else:
        event = random.choices(EVENTS, weights=[50,20,25,5])[0]
        ip = random.choice(IPS)
    return {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "user": user,
        "ip": ip,
        "event": event
    }

def main(num=200, delay=0.0):
    for _ in range(num):
        print(json.dumps(generate_log()))
        if delay:
            time.sleep(delay)

if __name__ == "__main__":
    # By default generate 200 lines quickly; when demoing, you can increase delay
    main(num=200, delay=0.01)
