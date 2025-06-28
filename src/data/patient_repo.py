from src.data.db import get_connection
from src.core.entities import Patient

def add_patient(patient: Patient) -> None:
    with get_connection() as conn:
        # Validate hospital exists
        rows = conn.execute(
            "SELECT 1 FROM doctors WHERE hospitaladdress = ?",
            (patient.nearesthospital,)
        ).fetchall()
        if not rows:
            raise ValueError("Nearest hospital does not match any doctor's hospitaladdress.")

        conn.execute('''
            INSERT INTO patients (firstname, lastname, address, phonenumber, nearesthospital)
            VALUES (?, ?, ?, ?, ?)
        ''', (
            patient.firstname, patient.lastname,
            patient.address, patient.phonenumber, patient.nearesthospital
        ))
        conn.commit()

def get_all_patients() -> list[tuple]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM patients").fetchall()
