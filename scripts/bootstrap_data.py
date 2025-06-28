# scripts/bootstrap_data.py

import sys
import os

# Add the root of the project to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))


from src.core.entities import Doctor, Patient
from src.data import doctor_repo, patient_repo

sample_hospitals = [
    "City General Hospital",
    "Green Valley Clinic",
    "Metro Health Center",
    "Lakeside Hospital"
]

def seed_doctors():
    doctors = [
        Doctor("John", "Smith", "MBBS", "Cardiologist", "123 Main St", sample_hospitals[0], "555-1234"),
        Doctor("Alice", "Brown", "MBBS, MD", "Neurologist", "234 Elm St", sample_hospitals[1], "555-2345"),
        Doctor("Robert", "White", "MBBS", "Dermatologist", "456 Oak St", sample_hospitals[2], "555-3456"),
        Doctor("Susan", "Clark", "MBBS", "Pediatrician", "789 Pine St", sample_hospitals[3], "555-4567"),
        Doctor("Tom", "Davis", "MBBS, MS", "Orthopedic", "321 Birch St", sample_hospitals[0], "555-5678"),
        Doctor("Laura", "King", "MBBS", "Psychiatrist", "654 Cedar St", sample_hospitals[1], "555-6789"),
        Doctor("James", "Hall", "MBBS", "ENT", "987 Maple St", sample_hospitals[2], "555-7890"),
        Doctor("Linda", "Allen", "MBBS", "Oncologist", "147 Spruce St", sample_hospitals[3], "555-8901"),
        Doctor("Henry", "Wright", "MBBS", "General Physician", "258 Cherry St", sample_hospitals[0], "555-9012"),
        Doctor("Emma", "Scott", "MBBS", "Gynecologist", "369 Aspen St", sample_hospitals[1], "555-0123"),
    ]

    for doc in doctors:
        doctor_repo.add_doctor(doc)
    print("✅ 10 sample doctors inserted.")


def seed_patients():
    firstnames = ["Mike", "Anna", "Tom", "Eva", "Jack", "Sara", "Bob", "Nina", "Ryan", "Lily",
                  "Kyle", "Maya", "Adam", "Ivy", "Luke", "Emma", "Jake", "Zoe", "Owen", "Kate"]
    lastnames = ["Turner", "Watson", "Lee", "Moore", "Young", "Hill", "Ward", "Fox", "Cole", "Gray",
                 "Stone", "Wells", "Black", "Grant", "Reed", "Shaw", "Day", "Bell", "Ross", "Cook"]

    for i in range(20):
        firstname = firstnames[i]
        lastname = lastnames[i]
        address = f"{100+i} Patient Ave"
        phone = f"777-10{i:02d}"
        nearest_hospital = sample_hospitals[i % len(sample_hospitals)]
        patient = Patient(firstname, lastname, address, phone, nearest_hospital)
        try:
            patient_repo.add_patient(patient)
        except ValueError as e:
            print(f"⚠️ Error inserting patient {firstname} {lastname}: {e}")
    print("✅ 20 sample patients inserted.")

if __name__ == "__main__":
    seed_doctors()
    seed_patients()
