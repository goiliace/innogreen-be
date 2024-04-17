from fastapi import APIRouter, FastAPI, Depends, status
from fastapi.responses import JSONResponse
from Chatbot import chatbot
from uuid import uuid4
from pydantic import BaseModel
from tools.tools import *

router = APIRouter()


@router.get('/history_chat')
async def get_history_chat(access_token: str = Depends(oauth2_scheme)):
    conn = create_connection()
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    token_data = decode_bearer_token(access_token)
    id_user, _ = get_user(conn, token_data.email)
    table_name = "history_chat"
    columns = 'id_his_chat,message, "user", "time"'
    select_query = f"SELECT {columns} FROM {table_name} WHERE id_user = '{id_user}' ORDER BY time DESC"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    all_chat = []
    for row in rows:
        chat = {row[0]:{
            "message": row[1],
            "user": row[2],
            "time": row[3]
        }}
        all_chat.append(chat)
    conn.close()
    return all_chat