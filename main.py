from tools.tools import *
from fastapi import FastAPI, UploadFile
from router import (chat, 
                    current_user,
                    get_question_patient,
                    # get_text_intro,
                    patients,
                    survey,
                    users,
                    get_all_patients)
import base64
import os
from fastapi.staticfiles import StaticFiles
from fastapi import FastAPI, __version__
from fastapi.responses import HTMLResponse
from dotenv import load_dotenv
from fastapi.middleware.cors import CORSMiddleware

load_dotenv('.env')

app = FastAPI()

origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/static", StaticFiles(directory="static"), name="static")

@app.get("/")
def router():
    return {"message": "API from Dumplings team project"}

@app.post("/uploadfile/")
async def create_upload_file(file: UploadFile):
    # convert file to base64 string
    base64_file = file.file.read()

    base64_file = base64.b64encode(base64_file).decode('utf-8')
    return {"filename": file.filename, "filetype": file.content_type, "base64_file": base64_file}

app.include_router(users.router)
app.include_router(current_user.router)
app.include_router(get_question_patient.router)
app.include_router(patients.router)
app.include_router(get_all_patients.router)
app.include_router(chat.router)
app.include_router(survey.router)
app.include_router(get_all_patients.router)


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=4040)	
