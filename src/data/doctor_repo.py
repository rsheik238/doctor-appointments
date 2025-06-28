from src.data.db import get_connection
from src.core.entities import Doctor

def add_doctor(doctor: Doctor) -> None:
    with get_connection() as conn:
        conn.execute('''
            INSERT INTO doctors (firstname, lastname, qualification, specialization, address, hospitaladdress, phone)
            VALUES (?, ?, ?, ?, ?, ?, ?)
        ''', (
            doctor.firstname, doctor.lastname, doctor.qualification,
            doctor.specialization, doctor.address, doctor.hospitaladdress, doctor.phone
        ))
        conn.commit()

def get_all_doctors() -> list[tuple]:
    with get_connection() as conn:
        return conn.execute("SELECT * FROM doctors").fetchall()
