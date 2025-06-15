"""Simple SQLite event logger."""

import sqlite3
from datetime import datetime


class EventLogger:
    def __init__(self, db_path: str = "events.db"):
        self.conn = sqlite3.connect(db_path, check_same_thread=False)
        self.conn.execute(
            "CREATE TABLE IF NOT EXISTS events(time TEXT, type TEXT, data TEXT)"
        )
        self.conn.commit()

    def log_event(self, event_type: str, data: str):
        timestamp = datetime.utcnow().isoformat()
        self.conn.execute(
            "INSERT INTO events(time, type, data) VALUES (?, ?, ?)",
            (timestamp, event_type, data),
        )
        self.conn.commit()
