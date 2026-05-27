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

        db.execute(text("""
            INSERT INTO Messages (MessageID, ConversationID, SenderRole, Message)
            VALUES (:id, :conv_id, 'User', :message)
        """), {
            "id": get_next_id(db, "Messages", "MessageID"),
            "conv_id": request.conversation_id,
            "message": user_message
        })

        db.execute(text("""
            INSERT INTO Messages (MessageID, ConversationID, SenderRole, Message)
            VALUES (:id, :conv_id, 'Assistant', :message)
        """), {
            "id": get_next_id(db, "Messages", "MessageID"),
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
        raise HTTPException(status_code=500, detail=f"Eroare: {str(e)}")

def get_next_id(db: Session, table: str, id_column: str) -> int:
    result = db.execute(text(f"SELECT ISNULL(MAX({id_column}), 0) + 1 FROM {table}")).fetchone()
    return result[0]