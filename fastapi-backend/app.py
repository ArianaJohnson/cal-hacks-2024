
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from uuid import uuid4, UUID
import mysql.connecter
from mysql.connector import Error

app = FastAPI()

# Database connection settings
DB_CONFIG = {
    "host": "your_singlestore_host",
    "user": "your_username",
    "password": "your_password",
    "database": "your_database"
}

# Model for emergency contact information
class EmergencyContact(BaseModel):
    name: str
    phone: str

# Model for medical information
class MedicalInfo(BaseModel):
    medical_conditions: List[str]
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None

# Model for a patient
class Patient(BaseModel):
    id: UUID
    name: str
    age: int
    emergency_contact: EmergencyContact
    medical_info: MedicalInfo

class DispatchRequest(BaseModel):
    patient_id: UUID
    emergency_type: str
    location: str
    additional_info: Optional[str] = None


# Get single store database
def get_db_connection():
    connection = mysql.connector.connect(**DB_CONFIG)
    return connection


#API post to create a paitnet
@app.post("/patients/", response_model=Patient)
async def create_patient(patient: Patient):
    patient.id = uuid4()
    query = """
    INSERT INTO patients (id, name, age, emergency_contact, medical_conditions, allergies, medications)
    VALUES (%s, %s, %s, %s, %s, %s, %s)
    """
    params = (
        str(patient.id),
        patient.name,
        patient.age,
        f"{patient.emergency_contact.name};{patient.emergency_contact.phone}",
        ', '.join(patient.medical_info.medical_conditions),
        ', '.join(patient.medical_info.allergies) if patient.medical_info.allergies else None,
        ', '.join(patient.medical_info.medications) if patient.medical_info.medications else None
    )
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            return patient
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

#Getapitent
@app.get("/patients/{patient_id}", response_model=Patient)
async def get_patient(patient_id: UUID):
    query = "SELECT * FROM patients WHERE id = %s"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
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



#Updates to the paitent informaiton
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
            cursor = conn.cursor()
            cursor.execute(query, params)
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Patient not found")
            return updated_patient
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

@app.post("/dispatch/", response_model=dict)
async def dispatch_request(dispatch: DispatchRequest):
    # Here, you can implement the logic to handle the dispatch,
    # such as sending alerts to emergency services or saving to a log.

    # For demonstration, we just log the dispatch information
    print(f"Dispatching for Patient ID: {dispatch.patient_id}")
    print(f"Emergency Type: {dispatch.emergency_type}")
    print(f"Location: {dispatch.location}")
    if dispatch.additional_info:
        print(f"Additional Info: {dispatch.additional_info}")

    # You might want to return a success message or details
    return {"message": "Dispatch request submitted successfully."}


@app.delete("/patients/{patient_id}", response_model=dict)
async def delete_patient(patient_id: UUID):
    query = "DELETE FROM patients WHERE id = %s"
    try:
        with get_db_connection() as conn:
            cursor = conn.cursor()
            cursor.execute(query, (str(patient_id),))
            conn.commit()
            if cursor.rowcount == 0:
                raise HTTPException(status_code=404, detail="Patient not found")
            return {"message": "Patient deleted successfully"}
    except Error as e:
        raise HTTPException(status_code=500, detail=str(e))

