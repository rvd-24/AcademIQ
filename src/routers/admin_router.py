from fastapi import APIRouter, Depends, HTTPException
from schemas.admin_schema import UploadMarksheet
from services.admin_service import upload_file_process
from db import get_db
from crud.student_crud import create_student_with_user, get_student_by_registration

router = APIRouter(prefix = "/api/admin", tags = ["admin"])

@router.get("/",method=['GET'])
def admin_home(request: HomeAdmin):
    ...


@router.post("/upload",method=['POST'])
def upload_marksheet(request: UploadMarksheet):
    file_name = request.file_name
    user_id = request.user_id
    file_status = upload_file_process()
    # TODO File Upload to Blob and LLM based extraction and DB Insertion
    return "File Uploaded Successfully"

@router.post("/register")
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
