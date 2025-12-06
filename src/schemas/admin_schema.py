from pydantic import BaseModel
from fastapi import UploadFile

class UploadMarksheet(BaseModel):
    file_name: str
    user_id: str
    file: UploadFile
    

class RegisterStudent(BaseModel):
    email: str
    password: str
    full_name: str
    registration_number: str
    department: str
    batch_year: int

class LoginStudent(BaseModel):
    email: str
    password: str

