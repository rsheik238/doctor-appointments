from src.core.entities import Patient
from src.data import patient_repo
import pandas as pd

def create_patient(data: dict) -> None:
    patient = Patient(**data)
    patient_repo.add_patient(patient)

def get_patients_df() -> pd.DataFrame:
    rows = patient_repo.get_all_patients()
    return pd.DataFrame(rows, columns=[
        "patientid", "firstname", "lastname", "address", "phonenumber", "nearesthospital"
    ])
