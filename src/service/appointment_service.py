from src.core.entities import Appointment
from src.data import appointment_repo
import pandas as pd

def create_appointment(data: dict) -> None:
    app = Appointment(**data)
    appointment_repo.add_appointment(app)

def get_appointments_df() -> pd.DataFrame:
    rows = appointment_repo.get_all_appointments()
    return pd.DataFrame(rows, columns=[
        "appointmentid", "doctor", "patient", "date", "time", "hospitaladdress"
    ])
