from fastapi import FastAPI, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from app.database import get_db, engine
from app import models

models.Base.metadata.create_all(bind=engine)

app = FastAPI(title="Student Records API")

YOUR_REG_NO = "2212204"


class StudentCreate(BaseModel):
    reg_no: str
    name: str
    email: str
    course: str


class StudentResponse(StudentCreate):
    id: int

    class Config:
        from_attributes = True


@app.get("/health")
def health_check(db: Session = Depends(get_db)):
    try:
        db.execute(text("SELECT 1"))
        db_status = "connected"
    except Exception:
        db_status = "disconnected"
    return {"status": "ok", "db": db_status, "student": YOUR_REG_NO}


@app.post("/students", response_model=StudentResponse, status_code=201)
def create_student(student: StudentCreate, db: Session = Depends(get_db)):
    db_student = models.Student(**student.model_dump())
    db.add(db_student)
    db.commit()
    db.refresh(db_student)
    return db_student


@app.get("/students", response_model=list[StudentResponse])
def get_students(db: Session = Depends(get_db)):
    return db.query(models.Student).all()


@app.get("/students/{reg_no}", response_model=StudentResponse)
def get_student(reg_no: str, db: Session = Depends(get_db)):
    student = db.query(models.Student).filter(
        models.Student.reg_no == reg_no
    ).first()
    if not student:
        raise HTTPException(status_code=404, detail="Student not found")
    return student
