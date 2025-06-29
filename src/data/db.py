# src/data/db.py
import sqlite3
import os
from pathlib import Path

# project-root = ../../.. from this file
BASE_DIR: Path = Path(__file__).resolve().parents[2]
DB_PATH: Path = BASE_DIR / "hospital.db"

def get_connection() -> sqlite3.Connection:
    # ALWAYS use the same absolute file
    return sqlite3.connect(DB_PATH)

def init_db():
    with get_connection() as conn:
        conn.execute("PRAGMA foreign_keys = ON")
        cur = conn.cursor()

        cur.execute('''
            CREATE TABLE IF NOT EXISTS doctors (
                doctorid INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                qualification TEXT,
                specialization TEXT,
                address TEXT,
                hospitaladdress TEXT NOT NULL,
                phone TEXT
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                patientid INTEGER PRIMARY KEY AUTOINCREMENT,
                firstname TEXT NOT NULL,
                lastname TEXT NOT NULL,
                address TEXT,
                phonenumber TEXT,
                nearesthospital TEXT NOT NULL,
                FOREIGN KEY (nearesthospital) REFERENCES doctors(hospitaladdress)
            )
        ''')

        cur.execute('''
            CREATE TABLE IF NOT EXISTS appointments (
                appointmentid INTEGER PRIMARY KEY AUTOINCREMENT,
                doctorid INTEGER NOT NULL,
                patientid INTEGER NOT NULL,
                date TEXT NOT NULL,
                time TEXT NOT NULL,
                hospitaladdress TEXT NOT NULL,
                FOREIGN KEY (doctorid) REFERENCES doctors(doctorid),
                FOREIGN KEY (patientid) REFERENCES patients(patientid)
            )
        ''')

        conn.commit()
