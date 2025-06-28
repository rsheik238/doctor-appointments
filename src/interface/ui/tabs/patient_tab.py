
# src/interface/ui/tabs/patient_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from datetime import datetime, timedelta
import pandas as pd
from src.service import get_doctors_df, get_patients_df, get_appointments_df, create_appointment

def get_doctor_slots():
    from datetime import datetime, timedelta
    slots = []
    current = datetime.strptime("09:00", "%H:%M")
    end = datetime.strptime("17:00", "%H:%M")
    lunch_start = datetime.strptime("12:00", "%H:%M")
    lunch_end = datetime.strptime("13:00", "%H:%M")
    while current < end and len(slots) < 16:
        if not (lunch_start <= current < lunch_end):
            slots.append(current.strftime("%H:%M"))
        current += timedelta(minutes=30)
    return slots

def format_name(row):
    return f"{row['lastname']}, {row['firstname']}"

def find_id_by_name(df, name):
    lastname, firstname = [x.strip() for x in name.split(',')]
    match = df[(df['lastname'] == lastname) & (df['firstname'] == firstname)]
    return int(match.iloc[0]['doctorid'] if 'doctorid' in match.columns else match.iloc[0]['patientid'])

def patient_tab(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text='Patients')

    doctor_df = get_doctors_df()
    doctor_names = [format_name(row) for _, row in doctor_df.iterrows()]

    patient_df = get_patients_df()
    patient_names = [format_name(row) for _, row in patient_df.iterrows()]

    # Booking Section
    ttk.Label(tab, text="Book Appointment").pack(pady=(10, 0))
    book_patient_combo = ttk.Combobox(tab, values=patient_names, state="readonly")
    book_patient_combo.pack()
    book_doctor_combo = ttk.Combobox(tab, values=doctor_names, state="readonly")
    book_doctor_combo.pack()
    book_date_picker = DateEntry(tab, date_pattern='yyyy-mm-dd')
    book_date_picker.pack()
    book_time_combo = ttk.Combobox(tab, values=get_doctor_slots(), state="readonly")
    book_time_combo.pack()

    def book():
        if not all([book_patient_combo.get(), book_doctor_combo.get(), book_date_picker.get(), book_time_combo.get()]):
            return messagebox.showerror("Missing", "All fields required.")
        pname = book_patient_combo.get()
        dname = book_doctor_combo.get()
        date = book_date_picker.get()
        time = book_time_combo.get()

        pid = find_id_by_name(patient_df, pname)
        did = find_id_by_name(doctor_df, dname)
        apt = get_appointments_df()
        booked = apt[(apt['doctor'] == dname) & (apt['date'] == date)]

        if len(booked) >= 16:
            return messagebox.showerror("Full", f"{dname} is fully booked on {date}")

        if time in booked['time'].values:
            used = set(booked['time'])
            for slot in get_doctor_slots():
                if slot not in used:
                    if messagebox.askyesno("Taken", f"{time} is taken. Book {slot} instead?"):
                        time = slot
                        break
                    else:
                        return
            else:
                return messagebox.showerror("No Slots", "No slots left.")

        addr = doctor_df[doctor_df['doctorid'] == did].iloc[0]['hospitaladdress']
        create_appointment({"doctorid": did, "patientid": pid, "date": date, "time": time, "hospitaladdress": addr})
        messagebox.showinfo("Booked", f"Appointment booked at {time} on {date}")

    ttk.Button(tab, text="Book", command=book).pack(pady=5)

    # View Appointments
    ttk.Label(tab, text="Select Patient:").pack()
    view_combo = ttk.Combobox(tab, values=patient_names, state="readonly")
    view_combo.pack()

    output = tk.Text(tab, height=15, width=100)
    output.pack(pady=10)

    def show():
        if not view_combo.get():
            return messagebox.showerror("Missing", "Select a patient.")
        name = view_combo.get()
        today = datetime.now().date()
        df = get_appointments_df()
        df['date'] = pd.to_datetime(df['date']).dt.date
        filtered = df[(df['patient'] == name) & (df['date'] >= today) & (df['date'] <= today + timedelta(days=30))]
        output.delete("1.0", tk.END)
        if filtered.empty:
            output.insert(tk.END, "No appointments found.")
        else:
            for _, row in filtered.iterrows():
                output.insert(tk.END, f"Doctor: {row['doctor']}, Date: {row['date']}, Time: {row['time']}\n")

    ttk.Button(tab, text="Show Appointments", command=show).pack(pady=5)

