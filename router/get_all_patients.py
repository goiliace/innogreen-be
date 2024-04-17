from tools.tools import *
from fastapi import  FastAPI,status ,APIRouter,Depends
from .current_user import *

router = APIRouter()
@router.get("/user/get_all_patients")
async def get_all_patients(access_token: str = Depends(oauth2_scheme)):
    # try:
        conn = create_connection()
        if conn is None:
            return {"error": "Failed to connect to the database"}
        token_data = decode_bearer_token(access_token)
        user_id,_ = get_user(conn, token_data.email)
        # user_id,_ = get_user(access_token)
        print(user_id)
        cursor = create_cursor(conn)
        cursor.execute("ROLLBACK")
        table_name = "patients"
        columns = "patient_id, name_patient, dob, address_patient, chart_params, note_case, detail, treatment, avatar"
        select_query = f"SELECT {columns} FROM {table_name} WHERE user_id = '{user_id}'"

        cursor.execute(select_query)
        rows = cursor.fetchall()
        patients = []
        for row in rows:
            patient = {
                "id_patients": row[0],
                "name_patient": row[1],
                "dob": row[2],
                "address_patient": row[3],
                "chart_params": row[4],
                "note_case": row[5],
                "detail": row[6],
                "treatment": row[7],
                "avatar": row[8]
            }
            patients.append(patient)
        conn.commit()
        conn.close()

        return {"patients": patients}

    # except Exception as e:
    #     return {"error": str(e),
    #             "id": user_id}