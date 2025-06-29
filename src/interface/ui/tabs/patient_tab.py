# ── src/interface/ui/tabs/patient_tab.py ──────────────────────────────
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta

import pandas as pd
from src.service import (
    get_doctors_df,
    get_patients_df,
    get_appointments_df,
    create_appointment,
    # you must implement these in appointment_service / repo
    delete_appointment,
)

from .utils import format_name, find_id_by_name, get_doctor_slots


# ───────────────────────────────────────────────────────────────────────
TODAY = datetime.now().date()


def patient_tab(notebook: ttk.Notebook) -> None:
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="Patients")

    # ── data ──
    doctor_df = get_doctors_df()
    patient_df = get_patients_df()
    doctor_names = [format_name(r) for _, r in doctor_df.iterrows()]
    patient_names = [format_name(r) for _, r in patient_df.iterrows()]

    # ── row-0  patient chooser ──
    r0 = ttk.Frame(tab)
    r0.pack(anchor="w")
    ttk.Label(r0, text="Patient:").pack(side="left", padx=(0, 4))
    cbo_patient = ttk.Combobox(r0, values=patient_names, state="readonly", width=30)
    cbo_patient.pack(side="left")

    # ── booking frame reused from earlier version (kept as-is) ──
    # ... you can leave your existing booking code here …

    # ── table header ──
    header_frame = ttk.Frame(tab, padding=(0, 10, 0, 2))
    header_frame.pack(fill="x")
    for idx, col in enumerate(("Date", "Time", "Doctor", "Cancel", "Reschedule")):
        ttk.Label(header_frame, text=col, width=12, anchor="w", font=("TkDefaultFont", 9, "bold")
                  ).grid(row=0, column=idx, sticky="w", padx=2)

    # ── table body container ──
    table_frame = ttk.Frame(tab)
    table_frame.pack(fill="x")

    # ───────────────────────────────────────────────────────────────────
    def _clear_table():
        for w in table_frame.winfo_children():
            w.destroy()

    def _refresh_table(*_):
        _clear_table()
        pname = cbo_patient.get()
        if not pname:
            return
        df = get_appointments_df()
        df["date"] = pd.to_datetime(df["date"]).dt.date
        future = df[(df["patient"] == pname) & (df["date"] <= TODAY + timedelta(days=60))]
        if future.empty:
            ttk.Label(table_frame, text="No appointments in next 2 months.").pack(anchor="w")
            return

        for row, (_, appt) in enumerate(future.sort_values(["date", "time"]).iterrows()):
            # --- static columns ---
            ttk.Label(table_frame, text=str(appt["date"]),  width=12).grid(row=row, column=0, sticky="w", padx=2)
            ttk.Label(table_frame, text=appt["time"],       width=8 ).grid(row=row, column=1, sticky="w", padx=2)
            ttk.Label(table_frame, text=appt["doctor"],     width=24).grid(row=row, column=2, sticky="w", padx=2)

            # --- action columns (future only) ---
            if appt["date"] >= TODAY:
                ttk.Button(
                    table_frame, text="Cancel",
                    command=lambda a_id=appt["appointmentid"]: _cancel(a_id)
                ).grid(row=row, column=3, padx=2)

                ttk.Button(
                    table_frame, text="Reschedule",
                    command=lambda a=appt: _reschedule_popup(a)
                ).grid(row=row, column=4, padx=2)
            else:
                ttk.Label(table_frame, text="–").grid(row=row, column=3)
                ttk.Label(table_frame, text="–").grid(row=row, column=4)

    # ── cancel handler ──
    def _cancel(app_id: int):
        if messagebox.askyesno("Confirm", "Cancel this appointment?"):
            delete_appointment(app_id)
            _refresh_table()

    # ── reschedule popup ──
    def _reschedule_popup(appt_row):
        pop = tk.Toplevel(tab)
        pop.title("Reschedule")
        pop.grab_set()

        ttk.Label(pop, text="New date:").grid(row=0, column=0, sticky="e", padx=4, pady=4)
        new_date = DateEntry(pop, date_pattern="yyyy-mm-dd", width=12)
        new_date.grid(row=0, column=1, sticky="w", padx=4, pady=4)

        ttk.Label(pop, text="New slot:").grid(row=1, column=0, sticky="e", padx=4, pady=4)
        slot_cbo = ttk.Combobox(pop, state="readonly", width=8)
        slot_cbo.grid(row=1, column=1, sticky="w", padx=4, pady=4)

        # populate slot dropdown whenever date changes
        def _load_slots(*_):
            slots_all = get_doctor_slots()
            df = get_appointments_df()
            taken = df[(df["doctor"] == appt_row["doctor"]) & (df["date"] == new_date.get())]["time"]
            free = [s for s in slots_all if s not in set(taken)]
            slot_cbo["values"] = free
            if free:
                slot_cbo.current(0)
        new_date.bind("<<DateEntrySelected>>", _load_slots)
        _load_slots()  # initial call

        # confirm button
        def _confirm():
            if not slot_cbo.get():
                return messagebox.showerror("Missing", "Choose a slot.")

            # delete old row
            delete_appointment(int(appt_row["appointmentid"]))

            # look-up IDs from names
            did = find_id_by_name(doctor_df, appt_row["doctor"])
            pid = find_id_by_name(patient_df, appt_row["patient"])

            # insert new row
            create_appointment(
                dict(
                    doctorid=did,
                    patientid=pid,
                    date=new_date.get(),
                    time=slot_cbo.get(),
                    hospitaladdress=appt_row["hospitaladdress"],
                )
            )

            pop.destroy()
            _refresh_table()

        ttk.Button(pop, text="Confirm", command=_confirm).grid(row=2, column=0, columnspan=2, pady=8)

    # ── wiring ──
    cbo_patient.bind("<<ComboboxSelected>>", _refresh_table)
