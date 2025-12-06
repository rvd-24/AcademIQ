from fastapi import APIRouter, Depends, HTTPException
from src.schemas.admin_schema import UploadMarksheet, RegisterStudent, LoginStudent
from src.services.admin_service import upload_file_process
from src.config.database import get_db as get_async_db
from sqlalchemy.ext.asyncio import AsyncSession
from src.crud.student_crud import create_student_with_user, get_student_by_registration
import asyncio


admin_router = APIRouter()


@admin_router.get("/")
async def admin_home():
    return "Backend Server is up and Running!"


@admin_router.post("/upload")
async def upload_marksheet(
    upload_marksheet: UploadMarksheet,
    db: AsyncSession = Depends(get_async_db)
):
    # Run the CPU / I/O heavy sync processing in a thread to avoid blocking the event loop
    upload_result = await asyncio.to_thread(upload_file_process, upload_marksheet.file)
    blob_url, extracted_content = upload_result['blob_url'], upload_result['extracted_json']
    return {"message": "File uploaded successfully", "marksheet_id": "1234567890", "extracted_content": extracted_content}


@admin_router.post("/register")
async def register_student(
    student: RegisterStudent,
    db: AsyncSession = Depends(get_async_db)
):
    """Register a new student"""
    try:
        student_obj = await create_student_with_user(
            db=db,
            email=student.email,
            password=student.password,
            full_name=student.full_name,
            registration_number=student.registration_number,
            department=student.department,
            batch_year=student.batch_year
        )
        return {"message": "Student registered successfully", "student_id": str(student_obj.student_id)}
    except Exception as e:
        import traceback
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Internal Server Error: {str(e)}")
