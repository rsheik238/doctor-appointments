import tkinter as tk
from tkinter import ttk, messagebox
from tkcalendar import DateEntry
from src.service import get_doctors_df, get_appointments_df
import pandas as pd

def format_name(row):
    return f"{row['lastname']}, {row['firstname']}"

def doctor_tab(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text='Doctors')

    doctor_df = get_doctors_df()
    doctor_names = [format_name(row) for _, row in doctor_df.iterrows()]

    ttk.Label(tab, text="Select Doctor:").pack(pady=5)
    doctor_combo = ttk.Combobox(tab, values=doctor_names, state="readonly")
    doctor_combo.pack()

    ttk.Label(tab, text="Select Date:").pack(pady=5)
    date_picker = DateEntry(tab, date_pattern='yyyy-mm-dd')
    date_picker.pack()

    output = tk.Text(tab, height=15, width=100)
    output.pack(pady=10)

    def show_appointments():
        if not doctor_combo.get():
            return messagebox.showerror("Error", "Select a doctor.")
        selected_date = date_picker.get()
        df = get_appointments_df()
        filtered = df[(df['doctor'] == doctor_combo.get()) & (df['date'] == selected_date)]
        output.delete("1.0", tk.END)
        if filtered.empty:
            output.insert(tk.END, "No appointments found.")
        else:
            for _, row in filtered.iterrows():
                output.insert(tk.END, f"Patient: {row['patient']}, Time: {row['time']}\n")

    ttk.Button(tab, text="Show Appointments", command=show_appointments).pack(pady=5)