
# src/interface/ui/main_ui.py
import tkinter as tk
from tkinter import ttk
from src.interface.ui.tabs.doctor_tab import doctor_tab
from src.interface.ui.tabs.patient_tab import patient_tab
from src.interface.ui.tabs.admin_tab import admin_tab

def main():
    root = tk.Tk()
    root.title("Hospital UI")
    root.geometry("900x600")

    notebook = ttk.Notebook(root)
    notebook.pack(expand=True, fill='both')

    doctor_tab(notebook)
    patient_tab(notebook)
    admin_tab(notebook)

    root.mainloop()

if __name__ == '__main__':
    main()
