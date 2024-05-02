from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

import schemas  
import crud  
import models  
from database import SessionLocal  

app = FastAPI()

# Dependency to get the database session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

# CRUD for Patients
@app.post("/patients/", response_model=schemas.Patient, status_code=status.HTTP_201_CREATED)
def create_patient(patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.create_patient(db, patient)

@app.get("/patients/{patient_id}", response_model=schemas.Patient)
def read_patient(patient_id: int, db: Session = Depends(get_db)):
    db_patient = crud.get_patient(db, patient_id)
    if not db_patient:
        raise HTTPException(status_code=404, detail="Patient not found")
    return db_patient

@app.put("/patients/{patient_id}", response_model=schemas.Patient)
def update_patient(patient_id: int, patient: schemas.PatientCreate, db: Session = Depends(get_db)):
    return crud.update_patient(db, patient_id, patient)

@app.delete("/patients/{patient_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_patient(patient_id: int, db: Session = Depends(get_db)):
    crud.delete_patient(db, patient_id)
    return {"detail": "Patient deleted"}

# CRUD for Doctors
@app.post("/doctors/", response_model=schemas.Doctor, status_code=status.HTTP_201_CREATED)
def create_doctor(doctor: schemas.DoctorCreate, db: Session = Depends(get_db)):
    return crud.create_doctor(db, doctor)

@app.get("/doctors/", response_model=List[schemas.Doctor])
def read_doctors(db: Session = Depends(get_db)):
    return crud.get_all_doctors(db)

@app.patch("/doctors/{doctor_id}/availability/", response_model=schemas.Doctor)
def set_doctor_availability(doctor_id: int, availability: schemas.DoctorAvailability, db: Session = Depends(get_db)):
    return crud.set_doctor_availability(db, doctor_id, availability.is_available)

@app.delete("/doctors/{doctor_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_doctor(doctor_id: int, db: Session = Depends(get_db)):
    crud.delete_doctor(db, doctor_id)
    return {"detail": "Doctor deleted"}

# Appointment Management
@app.post("/appointments/", response_model=schemas.Appointment)
def create_appointment(appointment: schemas.AppointmentCreate, db: Session = Depends(get_db)):
    return crud.create_appointment(db, appointment)

@app.patch("/appointments/{appointment_id}/complete", response_model=schemas.Appointment)
def complete_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return crud.complete_appointment(db, appointment_id)

@app.patch("/appointments/{appointment_id}/cancel", response_model=schemas.Appointment)
def cancel_appointment(appointment_id: int, db: Session = Depends(get_db)):
    return crud.cancel_appointment(db, appointment_id)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8000)
