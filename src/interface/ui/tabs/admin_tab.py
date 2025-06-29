# ── src/interface/ui/tabs/admin_tab.py ────────────────────────────────
import tkinter as tk
from tkinter import ttk
from tkcalendar import DateEntry
from datetime import datetime, timedelta

from src.service import get_doctors_df, get_appointments_df
from .utils import format_name, get_doctor_slots


# ───────────────────────────────────────────────────────────────────────
def admin_tab(notebook: ttk.Notebook) -> None:
    tab = ttk.Frame(notebook, padding=10)
    notebook.add(tab, text="Admin")

    # ░░ Data ░░
    doctor_df = get_doctors_df()
    doctor_names = [format_name(r) for _, r in doctor_df.iterrows()]
    slot_labels = get_doctor_slots()                       # 16 time strings

    # ░░ Row 1 – doctor ░░
    row1 = ttk.Frame(tab)
    row1.pack(anchor="w")
    ttk.Label(row1, text="Doctor:").pack(side="left", padx=(0, 4))
    cbo_doctor = ttk.Combobox(row1, values=doctor_names, state="readonly", width=30)
    cbo_doctor.pack(side="left")

    # ░░ Row 2 – date ░░
    row2 = ttk.Frame(tab)
    row2.pack(anchor="w", pady=(4, 0))
    ttk.Label(row2, text="Date:").pack(side="left", padx=(0, 24))
    cal_date = DateEntry(row2, date_pattern="yyyy-mm-dd", width=12)
    cal_date.pack(side="left")

    # ░░ Appointments list (time – patient) ░░
    txt_appts = tk.Text(tab, height=8, width=80, state="disabled")
    txt_appts.pack(fill="x", pady=(10, 6))

    # ░░ Patients frame ░░
    frm_patients = ttk.LabelFrame(tab, text="Patients", padding=8)
    frm_patients.pack(fill="x", pady=(6, 6))
    txt_patients = tk.Text(frm_patients, height=4, width=60, state="disabled")
    txt_patients.pack()

    # ░░ Slots frame – table ░░
    frm_slots = ttk.LabelFrame(tab, text="Available slots (next 7 days)", padding=8)
    frm_slots.pack(fill="both")
    grid_container = ttk.Frame(frm_slots)
    grid_container.pack()

    # style for grey ✖
    booked_style = ttk.Style()
    booked_style.configure("Booked.TLabel", foreground="grey")

    # ── helpers ────────────────────────────────────────────────────────
    def _clear_textboxes():
        for box in (txt_appts, txt_patients):
            box.configure(state="normal")
            box.delete("1.0", tk.END)

    def _draw_slot_grid(dname: str, start: datetime.date) -> None:
        # wipe previous grid
        for w in grid_container.winfo_children():
            w.destroy()

        # header row (time labels)
        ttk.Label(grid_container, text="", width=12).grid(row=0, column=0)  # top-left blank
        for c, t in enumerate(slot_labels, 1):
            ttk.Label(grid_container, text=t, width=6, anchor="center").grid(row=0, column=c, padx=1, pady=1)

        df = get_appointments_df()
        for r in range(7):
            day = start + timedelta(days=r)
            ttk.Label(grid_container, text=str(day), width=12, anchor="w").grid(
                row=r + 1, column=0, sticky="w", padx=2
            )

            day_taken = set(
                df[(df["doctor"] == dname) & (df["date"] == str(day))]["time"]
            )

            for c, slot in enumerate(slot_labels, 1):
                if slot in day_taken:
                    ttk.Label(
                        grid_container, text="✖", style="Booked.TLabel", width=6, anchor="center"
                    ).grid(row=r + 1, column=c, padx=1, pady=1)
                else:
                    ttk.Label(grid_container, text="", width=6).grid(row=r + 1, column=c, padx=1, pady=1)

    def _refresh(*_):
        dname = cbo_doctor.get()
        date_str = cal_date.get()

        _clear_textboxes()
        if not (dname and date_str):
            txt_appts.insert(tk.END, "Select doctor and date.")
            for box in (txt_appts, txt_patients):
                box.configure(state="disabled")
            return

        df = get_appointments_df()

        # appointments list
        daily = df[(df["doctor"] == dname) & (df["date"] == date_str)].sort_values("time")
        if daily.empty:
            txt_appts.insert(tk.END, "No appointments for this date.")
        else:
            for _, r in daily.iterrows():
                txt_appts.insert(tk.END, f"{r['time']}  –  {r['patient']}\n")

        # patient list
        unique_pat = sorted(df[df["doctor"] == dname]["patient"].unique())
        if unique_pat:
            for p in unique_pat:
                txt_patients.insert(tk.END, p + "\n")
        else:
            txt_patients.insert(tk.END, "None")

        # slot grid
        _draw_slot_grid(dname, datetime.strptime(date_str, "%Y-%m-%d").date())

        for box in (txt_appts, txt_patients):
            box.configure(state="disabled")

    # ── events ────────────────────────────────────────────────────────
    cbo_doctor.bind("<<ComboboxSelected>>", _refresh)
    cal_date.bind("<<DateEntrySelected>>", _refresh)
