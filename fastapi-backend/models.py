
from pydantic import BaseModel
from typing import List, Optional
from uuid  import UUID

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

# Model for dispatch requests
class DispatchRequest(BaseModel):
    patient_id: UUID
    emergency_type: str
    location: str
    additional_info: Optional[str] = None
