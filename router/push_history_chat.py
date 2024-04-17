from fastapi import APIRouter, FastAPI, Depends, status
from fastapi.responses import JSONResponse
from Chatbot import chatbot
from uuid import uuid4
from pydantic import BaseModel
from tools.tools import *

router = APIRouter()

class Message_content(BaseModel):
    message: str
    user: str
    time: datetime

@router.post('/push_history')
async def push_history_chat(content:Message_content ,access_token: str = Depends(oauth2_scheme)):
    conn = create_connection()
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    token_data = decode_bearer_token(access_token)
    id_user, _ = get_user(conn, token_data.email)
    table_name = "history_chat"
    columns = 'id_user,message, "user", "time"'
    insert_query = f'INSERT INTO {table_name} ({columns}) VALUES (%s, %s, %s, %s)'
    data_insert = (id_user, content.message, content.user, content.time)
    cursor.execute(insert_query, data_insert)
    conn.commit()
    conn.close()
    return {"message": "Insert history chat successfully"}