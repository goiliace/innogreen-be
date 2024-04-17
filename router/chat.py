import uvicorn
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
    # response = chatbot.Chatbot(str(uuid4()))
    print(message.message)
    # ans = response(message.message)
    ans = "highihi"
    return JSONResponse(content={"answer": message.message})