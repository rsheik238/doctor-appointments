# src/interface/ui/tabs/admin_tab.py
import tkinter as tk
from tkinter import ttk, messagebox
from src.service import get_doctors_df, get_appointments_df
import pandas as pd

def format_name(row):
    return f"{row['lastname']}, {row['firstname']}"

def admin_tab(notebook):
    tab = ttk.Frame(notebook)
    notebook.add(tab, text='Admin')

    doctor_df = get_doctors_df()
    doctor_names = [format_name(row) for _, row in doctor_df.iterrows()]

    ttk.Label(tab, text="Select Doctors:").pack()
    lb = tk.Listbox(tab, selectmode='multiple', height=10, width=50)
    for name in doctor_names:
        lb.insert(tk.END, name)
    lb.pack()

    output = tk.Text(tab, height=20, width=100)
    output.pack(pady=10)

    def show():
        indices = lb.curselection()
        if not indices:
            return messagebox.showerror("Error", "Select doctors.")
        selected = [doctor_names[i] for i in indices]
        df = get_appointments_df()
        filtered = df[df['doctor'].isin(selected)]
        output.delete("1.0", tk.END)
        if filtered.empty:
            output.insert(tk.END, "No appointments found.")
        else:
            for _, row in filtered.iterrows():
                output.insert(tk.END, f"Doctor: {row['doctor']}, Patient: {row['patient']}, Date: {row['date']}, Time: {row['time']}\n")

    ttk.Button(tab, text="Generate Report", command=show).pack(pady=5)

