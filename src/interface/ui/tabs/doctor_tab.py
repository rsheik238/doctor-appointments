# ── src/interface/ui/tabs/doctor_tab.py ───────────────────────────────
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime

from src.service import get_doctors_df, get_appointments_df
from .utils import format_name, get_doctor_slots


def doctor_tab(notebook: ttk.Notebook) -> None:
    """Create the Doctors tab (self-adding)."""
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="Doctors")

    # ░░ Data ░░
    doctor_df   = get_doctors_df()
    doctor_names = [format_name(r) for _, r in doctor_df.iterrows()]
    slot_labels  = get_doctor_slots()        # 16 slots

    # Row 0 – doctor picker
    row0 = ttk.Frame(tab)
    row0.pack(anchor="w")
    ttk.Label(row0, text="Doctor:").pack(side="left", padx=(0, 4))
    cbo_doctor = ttk.Combobox(row0, values=doctor_names, state="readonly", width=30)
    cbo_doctor.pack(side="left")

    # LabelFrame – Check appointments
    lf = ttk.LabelFrame(tab, text="Check appointments", padding=10)
    lf.pack(fill="x", pady=(10, 0))

    ttk.Label(lf, text="Date:").grid(row=0, column=0, sticky="e", pady=2)
    cal_date = DateEntry(lf, date_pattern="yyyy-mm-dd", width=12)
    cal_date.grid(row=0, column=1, sticky="w", pady=2)

    grid = ttk.Frame(lf)
    grid.grid(row=1, column=0, columnspan=2, pady=(8, 0))

    # Styles
    style = ttk.Style()
    style.configure("Available.TLabel", foreground="grey")
    style.configure("Booked.TLabel", foreground="black")

    # ── grid builder ──────────────────────────────────────────────────
    def _draw(dname: str, date_str: str) -> None:
        for w in grid.winfo_children():
            w.destroy()

        # header
        ttk.Label(grid, text="Time", width=8, anchor="center").grid(row=0, column=0, padx=2)
        ttk.Label(grid, text="Patient", width=30, anchor="center").grid(row=0, column=1, padx=2)

        df_day = get_appointments_df()
        df_day = df_day[(df_day["doctor"] == dname) & (df_day["date"] == date_str)]

        for r, slot in enumerate(slot_labels, start=1):
            ttk.Label(grid, text=slot, width=8, anchor="center").grid(row=r, column=0, padx=2, pady=1)

            match = df_day[df_day["time"] == slot]
            if match.empty:
                text, sty = " -- ", "Available.TLabel"
            else:
                text, sty = match.iloc[0]["patient"], "Booked.TLabel"

            ttk.Label(grid, text=text, style=sty, width=30, anchor="w").grid(
                row=r, column=1, sticky="w", padx=2, pady=1
            )

    # ── refresh triggers ──────────────────────────────────────────────
    def _refresh(*_):
        if cbo_doctor.get() and cal_date.get():
            _draw(cbo_doctor.get(), cal_date.get())

    cbo_doctor.bind("<<ComboboxSelected>>", _refresh)
    cal_date.bind("<<DateEntrySelected>>", _refresh)
