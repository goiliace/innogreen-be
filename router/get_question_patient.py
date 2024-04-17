# from tools import *
from tools.tools import *
from fastapi import  FastAPI, status, APIRouter, Depends
# from .current_user import *


class Patient_id(BaseModel):
    patient_id: str

router = APIRouter()
@router.get("/user/get_question_patient/", status_code=status.HTTP_201_CREATED)
async def get_question_patient(form_data: Patient_id, access_token: str = Depends(oauth2_scheme)): 
    conn = create_connection()
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    token_data = decode_bearer_token(access_token)
    patient_id = form_data.patient_id
    table_name = "patients"
    columns = "dob"
    select_query = f"SELECT {columns} FROM {table_name} WHERE patient_id = '{patient_id}'"
    cursor.execute(select_query)
    rows = cursor.fetchall()
    for row in rows:
        dob = row[0]
    num_month=calculate_month(dob)
    list_quest_id = [22,36,48,60]
    id_month = find_nearest_number(list_quest_id,num_month)
    questions = get_questions_by_patient_id(id_month)
    if not questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No questions found for the provided patient ID")
    
    return questions