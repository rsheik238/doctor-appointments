from dataclasses import dataclass
from typing import Optional

@dataclass
class Appointment:
    doctorid: int
    patientid: int
    date: str  # e.g., '2025-06-28'
    time: str  # e.g., '14:00'
    hospitaladdress: str
    appointmentid: Optional[int] = None
