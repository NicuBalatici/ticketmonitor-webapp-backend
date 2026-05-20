from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from sqlalchemy.testing import db

from database import get_db
import models

router = APIRouter()

@router.get("/")
def home():
    return {"status": "Serverul FastAPI este online!"}

@router.get("/test-db")
def test_database(db: Session = Depends(get_db)):
    try:
        result = db.execute(text("SELECT @@VERSION")).fetchone()
        return {
            "database_status": "Conectat cu succes!",
            "server_version": result[0]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare la conexiunea DB: {str(e)}")

@router.get("/api/tickets")
def get_fake_tickets(db: Session = Depends(get_db)):
    tickets = db.query(models.IncidentTicket).all()
    return tickets