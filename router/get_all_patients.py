from tools.tools import *
from fastapi import  FastAPI,status ,APIRouter,Depends
from .current_user import *

router = APIRouter()
@router.get("/get_all_patients/", status_code=status.HTTP_201_CREATED)
async def get_all_patients(access_token: str = Depends(oauth2_scheme)):
    try:
        user_id = get_user_id_from_token(access_token)
        conn = create_connection()
        if conn is None:
            return {"error": "Failed to connect to the database"}
        cur = conn.cursor()
        cur.execute("SELECT * FROM patients WHERE user_id = %s", (user_id,))
        rows = cur.fetchall()
        patients = []
        for row in rows:
            patient = {
                "id": row[0],
                "name": row[1],
                "age": row[2],
                "avatar": row[3],
                "note": row[4],
                "treatment": row[5], 
                "avatar": row[6],
                "detail": row[7]  
            }
            patients.append(patient)
        cur.close()
        conn.close()

        return {"patients": patients}

    except Exception as e:
        return {"error": str(e)}