import sqlite3
from pathlib import Path

DDL = (
    "CREATE TABLE IF NOT EXISTS projects("
    "id INTEGER PRIMARY KEY,"
    "source_system_id TEXT NOT NULL,"
    "source_name TEXT NOT NULL,"
    "title TEXT,"
    "jurisdiction TEXT,"
    "technology TEXT,"
    "capacity_mw REAL,"
    "developer TEXT,"
    "stage_text TEXT,"
    "status_date TEXT,"
    "location_text TEXT,"
    "lat REAL,"
    "lon REAL,"
    "url TEXT,"
    "raw_text TEXT,"
    "lead_flag TEXT,"
    "service_fit TEXT,"
    "first_seen TEXT,"
    "last_seen TEXT,"
    "UNIQUE(source_system_id, source_name)"
    ");"
)

class DB:
    def __init__(self, path: Path):
        self.conn = sqlite3.connect(str(path))
        self.conn.execute(DDL)
        self.conn.commit()

    def upsert_project(self, rec):
        fields = list(rec.keys())
        qmarks = ",".join(["?"] * len(fields))
        cols = ",".join(fields)
        updates = ",".join([f"{k}=excluded.{k}" for k in fields if k not in ("source_system_id","source_name","first_seen")])
        sql = (
            f"INSERT INTO projects ({cols}) VALUES ({qmarks}) "
            f"ON CONFLICT(source_system_id, source_name) DO UPDATE SET {updates};"
        )
        vals = [rec[k] for k in fields]
        self.conn.execute(sql, vals)
        self.conn.commit()
