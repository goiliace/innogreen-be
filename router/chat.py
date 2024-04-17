# import uvicorn
from fastapi import APIRouter, FastAPI, Depends, status
from fastapi.responses import JSONResponse
from Chatbot import chatbot
from uuid import uuid4
from pydantic import BaseModel
from tools.tools import *
# from .current_user import *

router = APIRouter()

class Message(BaseModel):
    message: str

@router.post('/chat/')
async def chat(message: Message, access_token: str = Depends(oauth2_scheme)):
    conn = create_connection()
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    token_data = decode_bearer_token(access_token)
    id_user, _ = get_user(conn, token_data.email)
    response = chatbot.Chatbot(id_user)
    table_name = "history_chat"
    columns='id_user,message,"user","time"'
    insert_query = f'INSERT INTO {table_name} ({columns}) VALUES (%s, %s, %s, %s)'
    data_insert_user = (id_user, message.message, "User", datetime.now())
    cursor.execute(insert_query, data_insert_user)
    # print(message.message)
    # print(response(message.message))
    ans = response(message.message)
    data_insert_bot = (id_user, ans, "Assistance", datetime.now())
    cursor.execute(insert_query, data_insert_bot)
    conn.commit()
    conn.close()
    return JSONResponse(content={"answer": ans})