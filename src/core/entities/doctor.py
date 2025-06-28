from dataclasses import dataclass
from typing import Optional

@dataclass
class Doctor:
    firstname: str
    lastname: str
    qualification: str
    specialization: str
    address: str
    hospitaladdress: str
    phone: str
    doctorid: Optional[int] = None  # Auto-incremented
