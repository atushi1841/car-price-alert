import sqlite3
import datetime
import json
import os

DB_PATH = os.environ.get("ALERT_DB", "alerts.db")

def get_conn():
    conn = sqlite3.connect(DB_PATH)
    conn.row_factory = sqlite3.Row
    return conn

def init_db():
    conn = get_conn()
    conn.execute("""CREATE TABLE IF NOT EXISTS alerts (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        model TEXT NOT NULL,
        max_price INTEGER,
        email TEXT NOT NULL,
        created_at TEXT,
        last_checked_at TEXT,
        last_found TEXT
    )""")
    conn.commit()
    conn.close()

def add_alert(model, max_price, email):
    conn = get_conn()
    created_at = datetime.datetime.now().isoformat()
    cur = conn.execute(
        "INSERT INTO alerts (model, max_price, email, created_at) VALUES (?,?,?,?)",
        (model, max_price, email, created_at)
    )
    conn.commit()
    new_id = cur.lastrowid
    conn.close()
    return new_id

def get_alerts():
    conn = get_conn()
    rows = conn.execute("SELECT * FROM alerts").fetchall()
    conn.close()
    return [dict(r) for r in rows]

def update_checked(alert_id, found_json_str):
    conn = get_conn()
    conn.execute(
        "UPDATE alerts SET last_checked_at = ?, last_found = ? WHERE id = ?",
        (datetime.datetime.now().isoformat(), found_json_str, alert_id)
    )
    conn.commit()
    conn.close()
