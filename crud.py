from sqlalchemy.orm import Session
from datetime import date
from fastapi import HTTPException
from schemas import PatientCreate
from schemas import DoctorCreate

import models
import schemas

def get_patient(db: Session, patient_id: int):
    """
    Retrieve a patient by ID.
    """
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def create_patient(db: Session, patient: schemas.PatientCreate):
    """
    Create a new patient and add to the database.
    """
    db_patient = models.Patient(**patient.dict())
    db.add(db_patient)
    db.commit()
    db.refresh(db_patient)
    return db_patient

def is_doctor_available(doctor_id: int, appointment_date: date, db: Session) -> bool:
    """
    Check if the doctor is available on a given date.
    """
    # Ensure only one appointment per doctor per day is scheduled
    return db.query(models.Appointment).filter(
        models.Appointment.doctor_id == doctor_id,
        models.Appointment.date == appointment_date,
        models.Appointment.status == "Scheduled"
    ).count() == 0

def create_appointment(db: Session, appointment: schemas.AppointmentCreate) -> models.Appointment:
    """
    Create a new appointment if the doctor is available.
    """
    if not is_doctor_available(appointment.doctor_id, appointment.date, db):
        raise HTTPException(status_code=400, detail="Doctor not available on this date")
    new_appointment = models.Appointment(**appointment.dict())
    db.add(new_appointment)
    db.commit()
    db.refresh(new_appointment)
    return new_appointment

def get_patient(db: Session, patient_id: int):
    return db.query(models.Patient).filter(models.Patient.id == patient_id).first()

def update_patient(db: Session, patient_id: int, patient_data: schemas.PatientCreate):
    db_patient = db.query(models.Patient).filter(models.Patient.id == patient_id).first()
    if db_patient:
        # Update model instance with new data
        for var, value in vars(patient_data).items():
            setattr(db_patient, var, value) if value else None
        db.commit()
        db.refresh(db_patient)
        return db_patient
    return None

def create_doctor(db: Session, doctor: schemas.DoctorCreate):
    db_doctor = models.Doctor(**doctor.dict())
    db.add(db_doctor)
    db.commit()
    db.refresh(db_doctor)
    return db_doctor

def complete_appointment(db: Session, appointment_id: int):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if appointment:
        appointment.status = 'Completed'
        appointment.doctor.is_available = True
        db.commit()
        return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")

def cancel_appointment(db: Session, appointment_id: int):
    appointment = db.query(models.Appointment).filter(models.Appointment.id == appointment_id).first()
    if appointment:
        appointment.status = 'Cancelled'
        appointment.doctor.is_available = True
        db.commit()
        return appointment
    raise HTTPException(status_code=404, detail="Appointment not found")

def set_doctor_availability(db: Session, doctor_id: int, is_available: bool):
    doctor = db.query(models.Doctor).filter(models.Doctor.id == doctor_id).first()
    if doctor:
        doctor.is_available = is_available
        db.commit()
        return doctor
    raise HTTPException(status_code=404, detail="Doctor not found")