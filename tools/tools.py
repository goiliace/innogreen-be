from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import BaseModel
from typing import Union, Annotated
from datetime import datetime, timedelta, timezone
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
import psycopg2
import os
from fastapi import  HTTPException, status, Depends, APIRouter, File, UploadFile, Form
import json

from dotenv import load_dotenv
load_dotenv('.env')


SECRET_KEY = os.getenv("SECRET_KEY")
ALGORITHM = os.getenv("ALGORITHM")
ACCESS_TOKEN_EXPIRE_MINUTES = 30
DB_NAME = os.getenv("DB_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

def verify_password(plain_password, hashed_password):
    return pwd_context.verify(plain_password, hashed_password)

# Function to hash the password
def get_password_hash(password):
    return pwd_context.hash(password)

def create_connection():
    try:
        conn = psycopg2.connect(database=DB_NAME,
                                user=DB_USER,
                                password=DB_PASS,
                                host=DB_HOST,
                                port=DB_PORT,
                                # pgbouncer=True
                                )
        print("Database connected successfully")
    except:
        print("Database not connected successfully")
    return conn

def create_cursor(conn):
    return conn.cursor()


class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Union[str, None] = None
    
class User(BaseModel):
    id: Union[str, None] = None
    email: str
    role: Union[str, None] = None
    full_name: Union[str, None] = None
    phone_number : Union[str, None] = None
    avatar : Union[str, None] = None
    gender : Union[bool, None] = None

class Patient(BaseModel):
    name_patient: Union[str, None] = None
    dob: Union[datetime, None] = None #sua lai thanh dob
    address_patient: Union[str, None] = None
    chart_params: Union[str, None] = None
    note_case: Union[str, None] = None
    detail: Union[str, None] = None
    treatment: Union[str, None] = None
    avatar: Union[UploadFile, None] = None
    @classmethod
    def as_form(
        cls,
        name_patient: str = Form(...),
        dob: datetime = Form(...),
        address_patient: str = Form(...),
        avatar: Union[UploadFile, None] = None
        
    ):
        return cls(
            name_patient=name_patient,
            dob=dob,
            address_patient=address_patient,
            avatar=avatar
        )

class PatientInDB(Patient):
    user_id : int 

class UserInDB(User):
    hashed_password: str

def decode_bearer_token(token: str):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
        return token_data
    except JWTError:
        raise credentials_exception


def get_user(conn, email: str):
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    result = cursor.fetchone()
    if result:
        return result[0],UserInDB(id=result[0],email=result[1],hashed_password=result[2],role=result[3],full_name=result[4],phone_number=result[5],avatar=result[6],gender=result[7])

def check_dupli_user_or_email(conn, email: str):
    cursor = create_cursor(conn)
    cursor.execute("ROLLBACK")
    cursor.execute(f"SELECT * FROM users WHERE email = '{email}'")
    result = cursor.fetchone()
    if result:
        return True
    else:
        return False    


def authenticate_user(conn, email: str, password: str):
    _,user = get_user(conn, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user

def create_access_token(data: dict, expires_delta: Union[timedelta, None] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_questions_by_patient_id(id_month):
    with open(r'data/questions_set.json', 'r', encoding="utf-8") as file:
        question_data = json.load(file)
    
    for patient_questions in question_data:
        for patient_key, questions in patient_questions.items():
            if patient_key == str(id_month):
                return questions
            
    return None

def calculate_month(dob):
    current_date = datetime.now()
    # dob = dob.replace(tzinfo=None)
    num_month = (current_date.year - dob.year) * 12 + current_date.month - dob.month
    # print(num_month)
    return num_month

def find_nearest_number(numbers, target):
    return min(numbers, key=lambda x: abs(x - target))