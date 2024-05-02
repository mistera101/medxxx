from pydantic import BaseModel
from datetime import date

# Patient schemas
class PatientBase(BaseModel):
    name: str
    age: int
    sex: str
    weight: float
    height: float
    phone: str

class PatientCreate(PatientBase):
    pass

class Patient(PatientBase):
    id: int
    class Config:
        from_attributes = True

# User schemas
class UserBase(BaseModel):
    username: str

class UserCreate(UserBase):
    password: str

class User(UserBase):
    id: int
    is_active: bool
    class Config:
        from_attributes = True


class Token(BaseModel):
    access_token: str
    token_type: str

# Appointment schemas
class AppointmentBase(BaseModel):
    patient_id: int
    doctor_id: int
    date: date
    status: str = "Scheduled"

class AppointmentCreate(AppointmentBase):
    pass

class Appointment(AppointmentBase):
    id: int
    class Config:
        from_attributes = True


class DoctorBase(BaseModel):
    name: str
    specialization: str
    phone: str
    is_available: bool = True

class DoctorCreate(DoctorBase):
    pass  

class Doctor(DoctorBase):
    id: int  
    class Config:
        from_attributes = True


class DoctorAvailability(BaseModel):
    is_available: bool
