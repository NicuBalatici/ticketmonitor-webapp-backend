from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db

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
def get_fake_tickets():
    return [
        {"id": 1, "title": "Nu merge imprimanta", "status": "Deschis", "priority": "High"},
        {"id": 2, "title": "Resetare parolă Active Directory", "status": "Închis", "priority": "Low"},
        {"id": 3, "title": "Eroare la conectare VPN", "status": "În progres", "priority": "Medium"}
    ]