from src.data.db import get_connection
from src.core.entities import Appointment

def add_appointment(app: Appointment) -> None:
    with get_connection() as conn:
        # Validate doctor and patient exist
        if not conn.execute("SELECT 1 FROM doctors WHERE doctorid = ?", (app.doctorid,)).fetchone():
            raise ValueError("Doctor ID not found.")
        if not conn.execute("SELECT 1 FROM patients WHERE patientid = ?", (app.patientid,)).fetchone():
            raise ValueError("Patient ID not found.")

        conn.execute('''
            INSERT INTO appointments (doctorid, patientid, date, time, hospitaladdress)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            app.doctorid, app.patientid, app.date, app.time, app.hospitaladdress
        ))
        conn.commit()

def get_all_appointments() -> list[tuple]:
    with get_connection() as conn:
        return conn.execute('''
            SELECT a.appointmentid, d.firstname || ' ' || d.lastname AS doctor,
                   p.firstname || ' ' || p.lastname AS patient,
                   a.date, a.time, a.hospitaladdress
            FROM appointments a
            JOIN doctors d ON a.doctorid = d.doctorid
            JOIN patients p ON a.patientid = p.patientid
        ''').fetchall()
