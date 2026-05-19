from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from ai_service import get_sql_from_question, get_natural_response

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
    
@router.post("/chat")
def chat(question: str, db: Session = Depends(get_db)):
    try:
        # 1. Obține SQL din întrebare
        sql_query = get_sql_from_question(question)

        # 2. Execută SQL și obține rezultate
        result = db.execute(text(sql_query)).fetchall()
        sql_result=str(result)  # Convertim rezultatul într-un string pentru a-l putea trimite la AI. Într-o aplicație reală, ar trebui să formatezi rezultatul mai frumos.

        # 3. Obține răspuns natural din rezultatul SQL
        natural_response = get_natural_response(question, sql_result)

        return {
            "sql_query": sql_query,
            "sql_result": sql_result,
            "natural_response": natural_response
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare: {str(e)}")