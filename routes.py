from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from sqlalchemy import text
from database import get_db
from pydantic import BaseModel
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

class ChatRequest(BaseModel):
    message: str
    conversation_id: int  
    user_id: int          

@router.post("/chat")
def chat(request: ChatRequest, db: Session = Depends(get_db)):
    try:
        user_message = request.message
        sql_query = ai_service.generate_sql(user_message)
        result = db.execute(text(sql_query)).fetchall()
        columns = ["Ticket_Number", "Status", "Priority"]
        data = [dict(zip(columns, row)) for row in result]
        ai_response = str(data)
        db.execute(text("""INSERT INTO Messages (MessageID, ConversationID, SenderRole, Message)
            VALUES (:id, :conv_id, 'User', :message)"""), {
            "id": get_next_id(db, "Messages", "MessageID"),
            "conv_id": request.conversation_id,
            "message": user_message
        })
        db.execute(text("""
            INSERT INTO Messages (MessageID, ConversationID, SenderRole, Message)
            VALUES (:id, :conv_id, 'Assistant', :message)"""), {
            "id": get_next_id(db, "Messages", "MessageID"),
            "conv_id": request.conversation_id,
            "message": ai_response
        })
        db.commit()  
        return {
            "user_message": user_message,
            "sql_generated": sql_query,
            "response": data
        }
    except Exception as e:
        db.rollback()  
        raise HTTPException(status_code=500, detail=str(e))


def get_next_id(db: Session, table: str, id_column: str) -> int:
    result = db.execute(text(f"SELECT ISNULL(MAX({id_column}), 0) + 1 FROM {table}")).fetchone()
    return result[0]
    
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