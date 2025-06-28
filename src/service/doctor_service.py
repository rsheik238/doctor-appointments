from src.core.entities import Doctor
from src.data import doctor_repo
import pandas as pd

def create_doctor(data: dict) -> None:
    doctor = Doctor(**data)
    doctor_repo.add_doctor(doctor)

def get_doctors_df() -> pd.DataFrame:
    rows = doctor_repo.get_all_doctors()
    return pd.DataFrame(rows, columns=[
        "doctorid", "firstname", "lastname", "qualification",
        "specialization", "address", "hospitaladdress", "phone"
    ])
