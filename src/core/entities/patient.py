from dataclasses import dataclass
from typing import Optional

@dataclass
class Patient:
    firstname: str
    lastname: str
    address: str
    phonenumber: str
    nearesthospital: str  # Must match a doctor’s hospitaladdress
    patientid: Optional[int] = None  # Auto-incremented
