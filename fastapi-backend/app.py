from fastapi import FastAPI, HTTPException
from typing import List, Optional
from uuid import uuid4, UUID
import psycopg2
from psycopg2 import sql, Error
from models import *
from gemini_fastapi import router as gemini_router

app = FastAPI()

# include the apis defined for gemini in another py
app.include_router(gemini_router)

# Database connection settings
DB_CONFIG = {
    "host": "your_postgres_host",
    "database": "medical_info_db",
    "user": "your_username",
    "password": "your_password",
}

# Helper function to get a database connection
def get_db_connection():
    return psycopg2.connect(**DB_CONFIG)

@app.post("/patients/", response_model=Patient)
async def create_patient(patient: Patient):
    query = """
    INSERT INTO patients (id, name, age, emergency_contact, medical_conditions, allergies, medications)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    RETURNING id
    """
    params = (
        str(uuid4()),  # Generate new UUID
        patient.name,
        patient.age,
        f"{patient.emergency_contact.name};{patient.emergency_contact.phone}",
        ', '.join(patient.medical_info.medical_conditions),
        ', '.join(patient.medical_info.allergies) if patient.medical_info.allergies else None,
        ', '.join(patient.medical_info.medications) if patient.medical_info.medications else None
    )

    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                patient.id = params[0]  # Assign generated UUID
                conn.commit()
                return patient
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients/{patient_id}", response_model=Patient)
async def get_patient(patient_id: UUID):
    query = "SELECT * FROM patients WHERE id = %s"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (str(patient_id),))
                row = cursor.fetchone()
                if row is None:
                    raise HTTPException(status_code=404, detail="Patient not found")
                return Patient(
                    id=row[0],
                    name=row[1],
                    age=row[2],
                    emergency_contact=EmergencyContact(*row[3].split(';')),
                    medical_info=MedicalInfo(
                        medical_conditions=row[4].split(', '),
                        allergies=row[5].split(', ') if row[5] else None,
                        medications=row[6].split(', ') if row[6] else None
                    )
                )
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.get("/patients/", response_model=List[Patient])
async def get_all_patients():
    query = "SELECT * FROM patients"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                return [
                    Patient(
                        id=row[0],
                        name=row[1],
                        age=row[2],
                        emergency_contact=EmergencyContact(*row[3].split(';')),
                        medical_info=MedicalInfo(
                            medical_conditions=row[4].split(', '),
                            allergies=row[5].split(', ') if row[5] else None,
                            medications=row[6].split(', ') if row[6] else None
                        )
                    ) for row in rows
                ]
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.put("/patients/{patient_id}", response_model=Patient)
async def update_patient(patient_id: UUID, updated_patient: Patient):
    query = """
    UPDATE patients
    SET name = %s, age = %s, emergency_contact = %s, medical_conditions = %s,
        allergies = %s, medications = %s
    WHERE id = %s
    """
    params = (
        updated_patient.name,
        updated_patient.age,
        f"{updated_patient.emergency_contact.name};{updated_patient.emergency_contact.phone}",
        ', '.join(updated_patient.medical_info.medical_conditions),
        ', '.join(updated_patient.medical_info.allergies) if updated_patient.medical_info.allergies else None,
        ', '.join(updated_patient.medical_info.medications) if updated_patient.medical_info.medications else None,
        str(patient_id)
    )
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, params)
                conn.commit()
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Patient not found")
                return updated_patient
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.delete("/patients/{patient_id}", response_model=dict)
async def delete_patient(patient_id: UUID):
    query = "DELETE FROM patients WHERE id = %s"
    try:
        with get_db_connection() as conn:
            with conn.cursor() as cursor:
                cursor.execute(query, (str(patient_id),))
                conn.commit()
                if cursor.rowcount == 0:
                    raise HTTPException(status_code=404, detail="Patient not found")
                return {"message": "Patient deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dispatch/", response_model=dict)
async def dispatch_request(dispatch: DispatchRequest):
    # Logic to handle the dispatch
    print(f"Dispatching for Patient ID: {dispatch.patient_id}")
    print(f"Emergency Type: {dispatch.emergency_type}")
    print(f"Location: {dispatch.location}")
    if dispatch.additional_info:
        print(f"Additional Info: {dispatch.additional_info}")
    return {"message": "Dispatch request submitted successfully."}

