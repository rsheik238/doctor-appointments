import sqlite3
import os

# Resolve DB path relative to the project root (not to this file)
BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../.."))
DB_PATH = os.path.join(BASE_DIR, "hospital.db")

def get_connection():
    return sqlite3.connect('hospital.db')

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
