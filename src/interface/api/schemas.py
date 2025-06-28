from pydantic import BaseModel, Field, validator
from typing import Optional


class DoctorIn(BaseModel):
    firstname: str = Field(..., min_length=1)
    lastname: str = Field(..., min_length=1)
    qualification: str
    specialization: str
    address: str
    hospitaladdress: str
    phone: str


class PatientIn(BaseModel):
    firstname: str
    lastname: str
    address: str
    phonenumber: str
    nearesthospital: str


class AppointmentIn(BaseModel):
    doctorid: int
    patientid: int
    date: str  # Format: YYYY-MM-DD
    time: str  # Format: HH:MM
    hospitaladdress: str
