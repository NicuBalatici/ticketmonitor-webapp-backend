from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from pydantic import BaseModel
from database import get_db

import ai_service
router = APIRouter()


# Modelul care se potrivește cu ce trimite React-ul (Chat.tsx)
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

        # 1. Obține SQL din întrebare (Folosind funcția Oliviei)
        sql_query = ai_service.get_sql_from_question(user_message)

        # 2. Verificare securitate - doar SELECT sau EXECUTE
        sql_upper = sql_query.strip().upper()
        if not (sql_upper.startswith("SELECT") or sql_upper.startswith("EXEC")):
            raise HTTPException(status_code=400, detail="Doar query-uri SELECT sunt permise!")
       
        # 3. Execută SQL și obține rezultatele din baza de date
        result = db.execute(text(sql_query)).fetchall()
        sql_result = str(result)

        # 4. Obține răspunsul natural de la AI (Folosind funcția Oliviei)
        ai_response = ai_service.get_natural_response(user_message, sql_result)

        # 5. Salvarea în baza de date (Logica originală din stânga)
        # Salvează mesajul utilizatorului
        db.execute(text("EXEC insertUserMessage :conv_id, :message"), {
            "conv_id": request.conversation_id,
            "message": user_message
        })
        db.execute(text("EXEC insertAssistantMessage :conv_id, :message"), {
            "conv_id": request.conversation_id,
            "message": ai_response
        })


        db.commit()

        # Trimitem pachetul final înapoi către React
        return {
            "user_message": user_message,
            "sql_query": sql_query,
            "sql_result": sql_result,
            "natural_response": ai_response
        }
    except HTTPException:
        raise
    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500, detail=f"Eroare: {str(e)}")

@router.get("/history/{conversation_id}")
def get_history(conversation_id: int, db: Session = Depends(get_db)):
    try:
        result = db.execute(text("""
            SELECT SenderRole, Message FROM Messages 
            WHERE ConversationID = :conv_id
            ORDER BY Sent_Datetime ASC
        """), {"conv_id": conversation_id}).fetchall()

        return [{"role": row[0].lower(), "text": row[1]} for row in result]
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Eroare: {str(e)}")