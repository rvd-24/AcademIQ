from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from schemas.admin_schema import UploadMarksheet
from services.admin_service import upload_file_process
from db import get_db
from sqlalchemy.orm import Session
from crud.student_crud import create_student_with_user, get_student_by_registration

admin_router = APIRouter()

@admin_router.get("/")
def admin_home():
    return "Backend Server is up and Running!"


@admin_router.post("/upload")
def upload_marksheet(
    file_name: str = Form(...),
    user_id: str = Form(...),
    file: UploadFile = File(...),
    db: Session = Depends(get_db)
):
    # file_name and user_id are now directly available as parameters
    upload_result = upload_file_process(file)
    blob_url, extracted_content = upload_result['blob_url'], upload_result['extracted_json']
    # marksheet_id = insert_marksheet_data(
    #     db=db,
    #     user_id=user_id,
    #     semester_number=semester_number,
    #     blob_url=blob_url,
    #     extracted_data=extracted_data
    # )
    return {"message": "File uploaded successfully", "marksheet_id": str(marksheet_id),"extracted_content":extracted_content}

@admin_router.post("/register")
async def register_student(
    email: str,
    password: str,
    full_name: str,
    registration_number: str,
    department: str,
    batch_year: int,
    db: Session = Depends(get_db)
):
    """Register a new student"""
    try:
        student = create_student_with_user(
            db=db,
            email=email,
            password=password,
            full_name=full_name,
            registration_number=registration_number,
            department=department,
            batch_year=batch_year
        )
        return student.to_dict()
    except Exception as e:
        raise HTTPException(status_code=400, detail=str(e))
