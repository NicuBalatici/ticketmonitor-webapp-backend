from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from database import get_db

import ai_service

router = APIRouter()

class ChatRequest(BaseModel):
    message: str
    conversation_id: int
    user_id: int

@router.get("/")
def home():
    return {"status": "Serverul FastAPI este online!"}

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        user_message = request.message

        sql_query = ai_service.get_sql_from_question(user_message)

        result = db.execute(text(sql_query)).fetchall()
        sql_result = str(result)

        ai_response = ai_service.get_natural_response(user_message, sql_result)

        # 4. Salvarea în baza de date (Logica originală din stânga)
        # Salvează mesajul utilizatorului
        db.execute(text("EXEC insertUserMessage :conv_id, :message"), {
            "conv_id": request.conversation_id,
            "message": user_message
        })

        # Salvează răspunsul AI-ului
        db.execute(text("EXEC insertAssistantMessage :conv_id, :message"), {
            "conv_id": request.conversation_id,
            "message": ai_response
        })

        db.commit()

        return {
            "user_message": user_message,
            "sql_query": sql_query,
            "sql_result": sql_result,
            "natural_response": ai_response
        }

    except Exception as e:
        db.rollback()
        print(str(e))
        raise HTTPException(status_code=500, detail=f"Eroare: {str(e)}")
