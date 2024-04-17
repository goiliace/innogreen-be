# from tools import *
from tools.tools import *
from fastapi import  FastAPI, status, APIRouter, Depends
# from .current_user import *


class Month(BaseModel):
    num_month: str

router = APIRouter()
@router.get("/get_question_patient/", status_code=status.HTTP_201_CREATED)
async def get_question_patient(id_patient: str, access_token: str = Depends(oauth2_scheme)): 
    db = create_connection()
    # Fetch patient from database
    patient = db.query(Patient).filter(Patient.id_patient == id_patient).first()
    db.close()

    if not patient:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Patient not found")

    try:
        patient_date = patient.dob
        num_month = patient_date.month
    except AttributeError:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Invalid patient record")

    questions = get_questions_by_patient_id(num_month)
    if not questions:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No questions found for the provided patient ID")
    
    return questions