"""
MediTrack Analytics – Synthetic Data Generator
Generates realistic data for your assignment
"""

import sqlite3
import random
import numpy as np
from datetime import date, timedelta

random.seed(42)
np.random.seed(42)

CITIES = ["Karachi", "Lahore", "Islamabad", "Peshawar", "Multan"]

CLINICS = {
    "Karachi": ["Aga Khan Clinic", "South City Medical", "Clifton Health Hub"],
    "Lahore": ["Shaukat Khanum Outpatient", "Gulberg Medical", "DHA Wellness"],
    "Islamabad": ["F-8 Medical Complex", "Blue Area Clinic", "Islamabad Diagnostic"],
    "Peshawar": ["Hayatabad Medical Hub", "Phase 4 Health Centre"],
    "Multan": ["Nishtar Outpatient", "Bosan Road Clinic", "Cantt Medical"]
}

DEPARTMENTS = ["General", "Cardiology", "Orthopedics", "Dermatology", "Pediatrics"]

FEE_RANGES = {
    "General": (800, 1500),
    "Cardiology": (2500, 5000),
    "Orthopedics": (2000, 4000),
    "Dermatology": (1500, 3000),
    "Pediatrics": (1000, 2000),
}

MALE_FIRST = ["Ahmed", "Muhammad", "Ali", "Hassan", "Usman", "Bilal", "Hamza"]
FEMALE_FIRST = ["Fatima", "Ayesha", "Zainab", "Maryam", "Sara", "Hina", "Amna"]
LAST_NAMES = ["Khan", "Malik", "Ahmed", "Hussain", "Chaudhry", "Siddiqui", "Baig"]

APPOINTMENT_TIMES = [
    "08:00", "08:30", "09:00", "09:30", "10:00", "10:30",
    "11:00", "11:30", "12:00", "14:00", "14:30", "15:00",
    "15:30", "16:00", "16:30", "17:00", "17:30", "18:00"
]

TIME_WEIGHTS = [
    4, 6, 9, 10, 9, 8,
    7, 6, 5, 6, 7, 8,
    9, 10, 8, 7, 6, 5
]

def random_name(gender="M"):
    first = random.choice(MALE_FIRST if gender == "M" else FEMALE_FIRST)
    last = random.choice(LAST_NAMES)
    return f"{first} {last}"

def generate_doctors():
    doctors = []
    doc_id = 1
    for city in CITIES:
        for dept in DEPARTMENTS:
            for _ in range(random.randint(3, 4)):
                gender = random.choice(["M", "F"])
                seniority = random.choice(["Junior", "Mid", "Senior", "Consultant"])
                base_fee = random.randint(*FEE_RANGES[dept])
                if seniority == "Senior":
                    base_fee = int(base_fee * 1.3)
                elif seniority == "Consultant":
                    base_fee = int(base_fee * 1.7)
                
                name = random_name(gender)
                title = "Prof. Dr." if seniority == "Consultant" else "Dr."
                
                doctors.append({
                    "doctor_id": doc_id,
                    "name": f"{title} {name}",
                    "department": dept,
                    "city": city,
                    "seniority": seniority,
                    "base_fee": base_fee,
                    "clinic": random.choice(CLINICS[city]),
                })
                doc_id += 1
    return doctors

def generate_patients(n=5000):
    patients = []
    for pid in range(1, n+1):
        gender = random.choice(["M", "F"])
        patients.append({
            "patient_id": pid,
            "name": random_name(gender),
            "gender": gender,
            "age": random.randint(8, 75),
            "city": random.choice(CITIES),
        })
    return patients

def generate_appointments(patients, doctors, n=25000):
    start_date = date(2024, 1, 1)
    end_date = date(2025, 6, 30)
    days = (end_date - start_date).days
    doctors_df = pd.DataFrame(doctors) if 'pandas' in globals() else None
    
    records = []
    seen = set()

    for _ in range(n):
        patient = random.choice(patients)
        is_new = patient["patient_id"] not in seen
        seen.add(patient["patient_id"])

        city = patient["city"] if random.random() < 0.8 else random.choice(CITIES)
        dept = random.choices(DEPARTMENTS, weights=[45, 14, 14, 14, 13])[0]

        matching = [d for d in doctors if d["city"] == city and d["department"] == dept]
        if not matching:
            matching = [d for d in doctors if d["department"] == dept]
        doctor = random.choice(matching)

        appt_date = start_date + timedelta(days=random.randint(0, days))
        # Reduce Sundays
        if appt_date.weekday() == 6 and random.random() < 0.7:
            appt_date = start_date + timedelta(days=random.randint(0, days))

        appt_time = random.choices(APPOINTMENT_TIMES, weights=TIME_WEIGHTS)[0]

        fee = int(doctor["base_fee"] * random.uniform(0.92, 1.08))

        # No-show probability
        prob = 0.13
        if is_new: prob += 0.11
        if appt_date.weekday() >= 5: prob += 0.09
        if dept in ["Dermatology", "Cardiology"]: prob += 0.06

        r = random.random()
        if r < prob:
            status = "no-show"
        elif r < prob + 0.11:
            status = "cancelled"
        else:
            status = "completed"

        records.append({
            "patient_id": patient["patient_id"],
            "doctor_id": doctor["doctor_id"],
            "department": dept,
            "city": city,
            "clinic": doctor["clinic"],
            "appointment_date": appt_date.isoformat(),
            "appointment_time": appt_time,
            "status": status,
            "is_new_patient": 1 if is_new else 0,
            "consultation_fee": fee if status == "completed" else 0,
        })
    return records

def main():
    print("⏳ Generating MediTrack data... This may take 15-25 seconds.")
    
    patients = generate_patients(5000)
    doctors = generate_doctors()
    appointments = generate_appointments(patients, doctors, 25000)

    print(f"✓ {len(patients):,} patients")
    print(f"✓ {len(doctors):,} doctors")
    print(f"✓ {len(appointments):,} appointments")

    conn = sqlite3.connect("meditrack.db")
    cur = conn.cursor()

    cur.executescript("""
        DROP TABLE IF EXISTS patients;
        DROP TABLE IF EXISTS doctors;
        DROP TABLE IF EXISTS appointments;
    """)

    cur.execute("""CREATE TABLE patients (
        patient_id INTEGER PRIMARY KEY,
        name TEXT,
        gender TEXT,
        age INTEGER,
        city TEXT
    )""")

    cur.execute("""CREATE TABLE doctors (
        doctor_id INTEGER PRIMARY KEY,
        name TEXT,
        department TEXT,
        city TEXT,
        seniority TEXT,
        base_fee INTEGER,
        clinic TEXT
    )""")

    cur.execute("""CREATE TABLE appointments (
        appointment_id INTEGER PRIMARY KEY AUTOINCREMENT,
        patient_id INTEGER,
        doctor_id INTEGER,
        department TEXT,
        city TEXT,
        clinic TEXT,
        appointment_date TEXT,
        appointment_time TEXT,
        status TEXT,
        is_new_patient INTEGER,
        consultation_fee INTEGER
    )""")

    cur.executemany("INSERT INTO patients VALUES (?,?,?,?,?)", 
                    [(p['patient_id'], p['name'], p['gender'], p['age'], p['city']) for p in patients])

    cur.executemany("INSERT INTO doctors VALUES (?,?,?,?,?,?,?)", 
                    [(d['doctor_id'], d['name'], d['department'], d['city'], d['seniority'], d['base_fee'], d['clinic']) for d in doctors])

    cur.executemany("""INSERT INTO appointments 
        (patient_id, doctor_id, department, city, clinic, appointment_date, appointment_time, status, is_new_patient, consultation_fee)
        VALUES (?,?,?,?,?,?,?,?,?,?)""", 
        [(a['patient_id'], a['doctor_id'], a['department'], a['city'], a['clinic'], 
          a['appointment_date'], a['appointment_time'], a['status'], a['is_new_patient'], a['consultation_fee']) for a in appointments])

    conn.commit()
    conn.close()

    print("\n✅ SUCCESS! meditrack.db has been created")
    print("   Total Appointments : 25,000")
    print("\nNext step: Run the dashboard with →  streamlit run app.py")

if __name__ == "__main__":
    main()
