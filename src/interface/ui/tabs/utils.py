# src/interface/ui/tabs/utils.py
"""
Shared helper functions for the Tkinter UI tabs.

Functions
---------
get_doctor_slots() -> list[str]
    Return the 30-minute time slots a doctor can accept in one day
    (9 :00–12 :00 and 13 :00–17 :00, up to 16 slots).

format_name(row: pd.Series) -> str
    Convert a doctors/patients DataFrame row to "Lastname, Firstname".

find_id_by_name(df: pd.DataFrame, name: str) -> int
    Look up doctorid/patientid in *df* by the formatted name.
"""

from __future__ import annotations

from datetime import datetime, timedelta
import pandas as pd


# ----------------------------------------------------------------------
# 1. Slot generator
# ----------------------------------------------------------------------
def get_doctor_slots() -> list[str]:
    """
    Generate at most 16 appointment slots of 30 min each:
      • Morning  : 09:00, 09:30, … 11:30
      • Lunch    : 12:00–13:00  (SKIPPED)
      • Afternoon: 13:00, 13:30, … 16:30
    """
    slots: list[str] = []
    current = datetime.strptime("09:00", "%H:%M")
    end     = datetime.strptime("17:00", "%H:%M")
    lunch_start = datetime.strptime("12:00", "%H:%M")
    lunch_end   = datetime.strptime("13:00", "%H:%M")

    while current < end and len(slots) < 16:
        if not (lunch_start <= current < lunch_end):
            slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)

    return slots


# ----------------------------------------------------------------------
# 2. Name formatter
# ----------------------------------------------------------------------
def format_name(row: pd.Series) -> str:
    """
    Return "Lastname, Firstname" from a DataFrame row that contains
    'firstname' and 'lastname' columns.
    """
    return f"{row['lastname']}, {row['firstname']}"


# ----------------------------------------------------------------------
# 3. ID finder by formatted name
# ----------------------------------------------------------------------
def find_id_by_name(df: pd.DataFrame, name: str) -> int:
    """
    Given a DataFrame *df* with firstname/lastname and the formatted
    string "Lastname, Firstname", return the corresponding numeric ID
    column ('doctorid' or 'patientid').

    Raises
    ------
    ValueError if the name is not found.
    """
    try:
        lastname, firstname = [part.strip() for part in name.split(",", 1)]
    except ValueError as exc:
        raise ValueError(f"Name '{name}' is not in 'Lastname, Firstname' form") from exc

    mask = (df["lastname"] == lastname) & (df["firstname"] == firstname)
    if mask.any():
        id_col = "doctorid" if "doctorid" in df.columns else "patientid"
        return int(df.loc[mask, id_col].iloc[0])

    raise ValueError(f"No match for '{name}' in DataFrame")
