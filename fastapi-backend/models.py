
from pydantic import BaseModel
from typing import List, Optional
from uuid  import UUID

# Model for emergency contact information
class EmergencyContact(BaseModel):
    name: str = None
    phone: str = None

# Model for medical information
class MedicalInfo(BaseModel):
    medical_conditions: List[str] = None
    allergies: Optional[List[str]] = None
    medications: Optional[List[str]] = None

# Model for a patient
class Patient(BaseModel):
    id: UUID = None
    name: str = None
    age: int = None
    emergency_contact: EmergencyContact = None
    medical_info: MedicalInfo = None

# Model for dispatch requests
class DispatchRequest(BaseModel):
    patient_id: UUID = None
    emergency_type: List[str] = None #can have a combination of police, ambulance, fire
    location: str = None
    additional_info: Optional[str] = None
